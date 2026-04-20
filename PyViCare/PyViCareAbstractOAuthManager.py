import logging
from abc import abstractmethod
from typing import Any

from authlib.integrations.base_client import TokenExpiredError, InvalidTokenError
from authlib.integrations.requests_client import OAuth2Session

from PyViCare import Feature
from PyViCare.PyViCareUtils import (PyViCareCommandError,
                                    PyViCareDeviceCommunicationError,
                                    PyViCareInternalServerError,
                                    PyViCareNotPaidForError,
                                    PyViCareRateLimitError)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

API_BASE_URL = 'https://api.viessmann-climatesolutions.com/iot/v2'
AUTHORIZE_URL = 'https://iam.viessmann-climatesolutions.com/idp/v3/authorize'
TOKEN_URL = 'https://iam.viessmann-climatesolutions.com/idp/v3/token'

SCOPE_IOT = "IoT"
SCOPE_USER = "User"
SCOPE_OFFLINE_ACCESS = "offline_access"
SCOPE_INTERNAL = "internal"


class AbstractViCareOAuthManager:
    def __init__(self, oauth_session: OAuth2Session) -> None:
        self.__oauth = oauth_session

    @property
    def oauth_session(self) -> OAuth2Session:
        return self.__oauth

    def replace_session(self, new_session: OAuth2Session) -> None:
        self.__oauth = new_session

    @classmethod
    @abstractmethod
    def renewToken(self) -> None:
        return

    def get(self, url: str) -> Any:
        try:
            logger.debug(self.__oauth)
            raw_response = self.__oauth.get(f"{API_BASE_URL}{url}", timeout=31)
            self.__raise_on_non_json_error(raw_response)
            response = raw_response.json()
            logger.debug("Response to get request: %s", response)
            self.__handle_expired_token(response)
            self.__handle_rate_limit(response)
            self.__handle_device_communication_error(response)
            self.__handle_not_paid_for(response)
            self.__handle_server_error(response)
            return response
        except TokenExpiredError:
            self.renewToken()
            return self.get(url)
        except InvalidTokenError:
            self.renewToken()
            return self.get(url)
        except OSError as e:
            raise PyViCareInternalServerError(
                {"statusCode": 0,
                 "message": str(e),
                 "viErrorId": "n/a"}) from e

    def __raise_on_non_json_error(self, response):
        """Guard against non-JSON error responses (e.g. 502 HTML pages from API gateway)."""
        if response.status_code >= 500:
            content_type = response.headers.get('content-type', '')
            if 'application/json' not in content_type:
                raise PyViCareInternalServerError(
                    {"statusCode": response.status_code,
                     "message": f"Non-JSON {response.status_code} response",
                     "viErrorId": "n/a"})

    def __handle_expired_token(self, response):
        if ("error" in response and response["error"] == "EXPIRED TOKEN"):
            raise TokenExpiredError(response)

    def __handle_rate_limit(self, response):
        if not Feature.raise_exception_on_rate_limit:
            return

        if ("statusCode" in response and response["statusCode"] == 429):
            raise PyViCareRateLimitError(response)

    def __handle_device_communication_error(self, response):
        if ("errorType" in response and response["errorType"] == "DEVICE_COMMUNICATION_ERROR"):
            raise PyViCareDeviceCommunicationError(response)

    def __handle_not_paid_for(self, response):
        if ("errorType" in response and response["errorType"] == "PACKAGE_NOT_PAID_FOR"):
            raise PyViCareNotPaidForError(response)

    def __handle_server_error(self, response):
        if ("statusCode" in response and response["statusCode"] >= 500):
            raise PyViCareInternalServerError(response)

        extended = response.get("extendedPayload", {})
        if isinstance(extended, dict) and extended.get("code") in ("500", "502", "503"):
            raise PyViCareInternalServerError(
                {"statusCode": int(extended["code"]),
                 "message": extended.get("reason", ""),
                 "viErrorId": response.get("viErrorId", "n/a")})

    def __handle_command_error(self, response):
        if not Feature.raise_exception_on_command_failure:
            return

        if ("statusCode" in response and response["statusCode"] >= 400):
            raise PyViCareCommandError(response)

    def post(self, url, data) -> Any:
        """POST URL using OAuth session. Automatically renew the token if needed
        Parameters
        ----------
        url : str
            URL to get
        data : str
            Data to post

        Returns
        -------
        result: json
            json representation of the answer
        """
        headers = {"Content-Type": "application/json",
                   "Accept": "application/vnd.siren+json"}
        try:
            raw_response = self.__oauth.post(
                f"{API_BASE_URL}{url}", data, headers=headers)
            self.__raise_on_non_json_error(raw_response)
            response = raw_response.json()
            self.__handle_expired_token(response)
            self.__handle_rate_limit(response)
            self.__handle_command_error(response)
            return response
        except TokenExpiredError:
            self.renewToken()
            return self.post(url, data)
        except InvalidTokenError:
            self.renewToken()
            return self.post(url, data)
        except OSError as e:
            raise PyViCareInternalServerError(
                {"statusCode": 0,
                 "message": str(e),
                 "viErrorId": "n/a"}) from e
