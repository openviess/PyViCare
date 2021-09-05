import logging

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareBrowserOAuthManager import ViCareBrowserOAuthManager
from PyViCare.PyViCareCachedService import ViCareCachedService
from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareOAuthManager import ViCareOAuthManager
from PyViCare.PyViCareService import ViCareDeviceAccessor, ViCareService
from PyViCare.PyViCareUtils import PyViCareInvalidDataError

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

""""Viessmann ViCare API Python tools"""


class PyViCare:
    def __init__(self) -> None:
        self.cacheDuration = 60

    def setCacheDuration(self, cache_duration):
        self.cacheDuration = cache_duration

    def initWithCredentials(self, username: str, password: str, client_id: str, token_file: str):
        self.initWithExternalOAuth(ViCareOAuthManager(
            username, password, client_id, token_file))

    def initWithExternalOAuth(self, oauth_manager: AbstractViCareOAuthManager) -> None:
        self.oauth_manager = oauth_manager
        self.__loadInstallations()

    def initWithBrowserOAuth(self, client_id: str, token_file: str) -> None:
        self.initWithExternalOAuth(ViCareBrowserOAuthManager(client_id, token_file))

    def __buildService(self, accessor):
        if self.cacheDuration > 0:
            return ViCareCachedService(self.oauth_manager, accessor, self.cacheDuration)
        else:
            return ViCareService(self.oauth_manager, accessor)

    def __loadInstallations(self):
        installations = self.oauth_manager.get(
            "/equipment/installations?includeGateways=true")
        if "data" not in installations:
            logger.error("Missing 'data' property when fetching installations")
            raise PyViCareInvalidDataError(installations)

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
