from PyViCare import Feature
from PyViCare.PyViCareUtils import PyViCareRateLimitError
from abc import abstractclassmethod
from oauthlib.oauth2 import TokenExpiredError
import logging

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

API_BASE_URL = 'https://api.viessmann.com/iot/v1'


class AbstractViCareOAuthManager:
    def __init__(self):
        self.oauth = None

    @abstractclassmethod
    def renewToken(self):
        return

    def get(self, url):
        try:
            logger.debug(self.oauth)
            response = self.oauth.get(f"{API_BASE_URL}{url}").json()
            logger.debug("Response to get request: "+str(response))
            self.handleExpiredToken(response)
            self.handleRateLimit(response)
            return response
        except TokenExpiredError:
            self.renewToken()
            return self.get(url)

    def handleExpiredToken(self, response):
        if("error" in response and response["error"] == "EXPIRED TOKEN"):
            raise TokenExpiredError(response)

    def handleRateLimit(self, response):
        if not Feature.raise_exception_on_rate_limit:
            return

        if("statusCode" in response and response["statusCode"] == 429):
            raise PyViCareRateLimitError(response)

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

    def post(self, url, data):
        headers = {"Content-Type": "application/json",
                   "Accept": "application/vnd.siren+json"}
        try:
            response = self.oauth.post(
                f"{API_BASE_URL}{url}", data, headers=headers).json()
            self.handleExpiredToken(response)
            self.handleRateLimit(response)
            return response
        except TokenExpiredError:
            self.renewToken()
            return self.post(url, data)
