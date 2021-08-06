from PyViCare.PyViCareBrowserOAuthManager import ViCareBrowserOAuthManager
from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareOAuthManager import ViCareOAuthManager
from PyViCare.PyViCareService import ViCareDeviceAccessor, ViCareService
from PyViCare.PyViCareCachedService import ViCareCachedService
import logging

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

""""Viessmann ViCare API Python tools"""


class PyViCare:
    def __init__(self):
        self.cacheDuration = 60

    def setCacheDuration(self, cache_duration):
        self.cacheDuration = cache_duration

    def initWithCredentials(self, username, password, client_id, token_file):
        self.oauth_manager = ViCareOAuthManager(
            username, password, client_id, token_file)
        self.__loadInstallations()

    def initWithExternalOAuth(self, oauth_manager):
        self.oauth_manager = oauth_manager
        self.__loadInstallations()

    def initWithBrowserOAuth(self, client_id, token_file):
        self.oauth_manager = ViCareBrowserOAuthManager(client_id, token_file)
        self.__loadInstallations()

    def __buildService(self, accessor):
        if self.cacheDuration > 0:
            return ViCareCachedService(self.oauth_manager, accessor, self.cacheDuration)
        else:
            return ViCareService(self.oauth_manager, accessor)

    def __loadInstallations(self):
        installations = self.oauth_manager.get(
            "/equipment/installations?includeGateways=true")
        self.devices = list(self.__readInstallations(installations["data"]))

    def __readInstallations(self, data):
        for installation in data:
            installation_id = installation["id"]

            for gateway in installation["gateways"]:
                gateway_serial = gateway["serial"]

                for device in gateway["devices"]:
                    if device["deviceType"] != "heating":
                        continue  # we are not interested in non heating devices

                    device_id = device["id"]
                    device_model = device["modelId"]
                    status = device["status"]

                    accessor = ViCareDeviceAccessor(
                        installation_id, gateway_serial, device_id)
                    service = self.__buildService(accessor)

                    logger.info(f"Device found: {device_model}")

                    yield PyViCareDeviceConfig(service, device_model, status)
