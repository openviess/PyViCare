import logging
from datetime import datetime

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareBrowserOAuthManager import ViCareBrowserOAuthManager
from PyViCare.PyViCareCachedService import ViCareCachedService
from PyViCare.PyViCareCachedServiceViaGateway import ViCareCachedServiceViaGateway
from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareOAuthManager import ViCareOAuthManager
from PyViCare.PyViCareService import ViCareDeviceAccessor, ViCareService
from PyViCare.PyViCareServiceViaGateway import ViCareServiceViaGateway
from PyViCare.PyViCareUtils import PyViCareInvalidDataError

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

def __buildService(oauth_manager, cacheDuration, viaGateway: bool, accessor, roles):
    if cacheDuration > 0:
        if viaGateway:
            return ViCareCachedServiceViaGateway(oauth_manager, accessor, roles, cacheDuration)
        return ViCareCachedService(oauth_manager, accessor, roles, cacheDuration)

    if viaGateway:
        return ViCareServiceViaGateway(oauth_manager, accessor, roles)
    return ViCareService(oauth_manager, accessor, roles)

class PyViCare:
    viaGateway = False

    """"Viessmann ViCare API Python tools"""
    def __init__(self) -> None:
        self.cacheDuration = 60

    def setCacheDuration(self, cache_duration):
        self.cacheDuration = int(cache_duration)

    def loadViaGateway(self, via_gateway: bool = True) -> None:
        self.viaGateway = via_gateway

    def initWithCredentials(self, username: str, password: str, client_id: str, token_file: str):
        self.initWithExternalOAuth(ViCareOAuthManager(
            username, password, client_id, token_file))

    def initWithExternalOAuth(self, oauth_manager: AbstractViCareOAuthManager) -> None:
        self.oauth_manager = oauth_manager
        self.__loadInstallations()

    def initWithBrowserOAuth(self, client_id: str, token_file: str) -> None:
        self.initWithExternalOAuth(ViCareBrowserOAuthManager(client_id, token_file))

    def __loadInstallations(self):
        installations = self.oauth_manager.get(
            "/equipment/installations?includeGateways=true")
        if "data" not in installations:
            logger.error("Missing 'data' property when fetching installations")
            raise PyViCareInvalidDataError(installations)

        self.installations = Wrap(installations["data"])
        self.devices = list(self.__extract_devices())

    def __extract_devices(self):
        for installation in self.installations:
            for gateway in installation.gateways:
                if self.viaGateway:
                    service = __buildService

                for device in gateway.devices:
                    if device.deviceType not in ["heating", "zigbee", "vitoconnect", "electricityStorage", "tcu", "ventilation"]:
                        continue  # we are only interested in heating, photovoltaic, electricityStorage, and ventilation devices

                    accessor = ViCareDeviceAccessor(
                        installation.id, gateway.serial, device.id)
                    service = __buildService(self.oauth_manager, self.cacheDuration, self.viaGateway, accessor, device.roles)

                    logger.info("Device found: %s", device.modelId)

                    yield PyViCareDeviceConfig(service, device.id, device.modelId, device.status, device.deviceType, device.roles)


class DictWrap(object):
    def __init__(self, d):
        for k, v in d.items():
            setattr(self, k, Wrap(v))


def Wrap(v):
    if isinstance(v, list):
        return [Wrap(x) for x in v]
    if isinstance(v, dict):
        return DictWrap(v)
    if isinstance(v, str) and len(v) == 24 and v[23] == 'Z' and v[10] == 'T':
        return datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f%z')
    return v
