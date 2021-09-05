import logging
from abc import abstractclassmethod
from typing import Any

from oauthlib.oauth2 import TokenExpiredError  # type: ignore
from requests_oauthlib.oauth2_session import OAuth2Session

from PyViCare import Feature
from PyViCare.PyViCareUtils import (PyViCareCommandError,
                                    PyViCareInternalServerError,
                                    PyViCareRateLimitError)

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

API_BASE_URL = 'https://api.viessmann.com/iot/v1'


class AbstractViCareOAuthManager:
    def __init__(self, oauth_session: OAuth2Session) -> None:
        self.__oauth = oauth_session

    @property
    def oauth_session(self) -> OAuth2Session:
        return self.__oauth

    def replace_session(self, new_session: OAuth2Session) -> None:
        self.__oauth = new_session

    @abstractclassmethod
    def renewToken(self):
        return

    def get(self, url: str) -> Any:
        try:
            logger.debug(self.__oauth)
            response = self.__oauth.get(f"{API_BASE_URL}{url}").json()
            logger.debug(f"Response to get request: {response}")
            self.__handle_expired_token(response)
            self.__handle_rate_limit(response)
            self.__handle_server_error(response)
            return response
        except TokenExpiredError:
            self.renewToken()
            return self.get(url)

    def __handle_expired_token(self, response):
        if("error" in response and response["error"] == "EXPIRED TOKEN"):
            raise TokenExpiredError(response)

    def __handle_rate_limit(self, response):
        if not Feature.raise_exception_on_rate_limit:
            return

        if("statusCode" in response and response["statusCode"] == 429):
            raise PyViCareRateLimitError(response)

    def __handle_server_error(self, response):
        if("statusCode" in response and response["statusCode"] >= 500):
            raise PyViCareInternalServerError(response)

    def __handle_command_error(self, response):
        if not Feature.raise_exception_on_command_failure:
            return

        if("statusCode" in response and response["statusCode"] >= 400):
            raise PyViCareCommandError(response)

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

    def post(self, url, data) -> Any:
        headers = {"Content-Type": "application/json",
                   "Accept": "application/vnd.siren+json"}
        try:
            response = self.__oauth.post(
                f"{API_BASE_URL}{url}", data, headers=headers).json()
            self.__handle_expired_token(response)
            self.__handle_rate_limit(response)
            self.__handle_command_error(response)
            return response
        except TokenExpiredError:
            self.renewToken()
            return self.post(url, data)
