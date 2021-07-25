from oauthlib.oauth2 import TokenExpiredError
import logging

# This is required because "requests" uses simplejson if installed on the system

import simplejson as json
from PyViCare.PyViCare import PyViCareNotSupportedFeatureError, PyViCareRateLimitError
import PyViCare.Feature

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

apiURLBase = 'https://api.viessmann.com/iot/v1'


def readFeature(entities, property_name):
    feature = next(
        (f for f in entities if f["feature"] == property_name), None)

    if(feature is None):
        raise PyViCareNotSupportedFeatureError(property_name)

    return feature


def buildSetPropertyUrl(id, serial, circuit, property_name, action):
    return apiURLBase + '/equipment/installations/'+str(id)+'/gateways/'+str(serial)+'/devices/'+str(circuit)+'/features/'+property_name+'/'+action


def buildGetPropertyUrl(id, serial, circuit, property_name):
    return apiURLBase + '/equipment/installations/'+str(id)+'/gateways/'+str(serial)+'/devices/'+str(circuit)+'/features/'+property_name


""""Viessmann ViCare API Python tools"""


class ViCareService:
    """This class connects to the Viesmann ViCare API.
    The authentication is done through OAuth2.
    Note that currently, a new token is generate for each run.
    """

    def __init__(self, oauth_manager, circuit):
        self.oauth_manager = oauth_manager
        self.circuit = circuit
        self._getInstallations()
        logger.info("Initialisation successful !")

    """Get URL using OAuth session. Automatically renew the token if needed
    Parameters
    ----------
    url : str
        URL to get

    Returns
    -------
    result: json
        json representation of the answer
    """

    def __get(self, url):
        try:
            logger.debug(self.oauth)
            response = self.oauth_manager.get(url).json()
            logger.debug("Response to get request: "+str(response))
            self.handleExpiredToken(response)
            self.handleRateLimit(response)
            return response
        except TokenExpiredError:
            self.renewToken()
            return self.__get(url)

    def handleExpiredToken(self, response):
        if("error" in response and response["error"] == "EXPIRED TOKEN"):
            raise TokenExpiredError(response)

    def handleRateLimit(self, response):
        if not PyViCare.Feature.raise_exception_on_rate_limit:
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

    def __post(self, url, data):
        headers = {"Content-Type": "application/json",
                   "Accept": "application/vnd.siren+json"}
        try:
            response = self.oauth_manager.post(
                url, data, headers=headers).json()
            self.handleExpiredToken(response)
            self.handleRateLimit(response)
            return response
        except TokenExpiredError:
            self.oauth_manager.renewToken()
            return self.__post(url, data)

    def _getInstallations(self):
        self.installations = self.__get(
            apiURLBase+"/equipment/installations?includeGateways=true")
        installation = self.installations["data"][0]
        self.id = installation["id"]
        self.serial = installation["gateways"][0]["serial"]

        return self.installations

    def getInstallations(self):
        return self.installations

    def get(self, url):
        return self.__get(url)

    def getProperty(self, property_name):
        url = buildGetPropertyUrl(
            self.id, self.serial, self.circuit, property_name)
        j = self.__get(url)
        return j

    def setProperty(self, property_name, action, data):
        url = buildSetPropertyUrl(
            self.id, self.serial, self.circuit, property_name, action)
        return self.__post(url, data)
