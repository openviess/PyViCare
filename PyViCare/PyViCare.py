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

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PyViCare:
    """"Viessmann ViCare API Python tools"""
    viaGateway = False

    def __init__(self) -> None:
        self.cacheDuration = 60

    def setCacheDuration(self, cache_duration):
        self.cacheDuration = int(cache_duration)

    def loadViaGateway(self, via_gateway: bool = True) -> None:
        """Opt in to per-gateway bulk fetching.

        When enabled, ONE service instance per gateway serves all devices on
        that gateway via the bulk endpoint
        `/features/installations/{id}/gateways/{serial}/features?includeDevicesFeatures=true`,
        instead of one HTTP call per device per refresh. Must be called
        before initWith* (services are wired during __loadInstallations).
        """
        self.viaGateway = via_gateway

    def initWithCredentials(self, username: str, password: str, client_id: str, token_file: str):
        self.initWithExternalOAuth(ViCareOAuthManager(
            username, password, client_id, token_file))

    def initWithExternalOAuth(self, oauth_manager: AbstractViCareOAuthManager) -> None:
        self.oauth_manager = oauth_manager
        self.__loadInstallations()

    def initWithBrowserOAuth(self, client_id: str, token_file: str) -> None:
        self.initWithExternalOAuth(ViCareBrowserOAuthManager(client_id, token_file))

    def __buildService(self, roles):
        if self.cacheDuration > 0:
            return ViCareCachedService(self.oauth_manager, roles, self.cacheDuration)
        return ViCareService(self.oauth_manager, roles)

    def __buildGatewayService(self):
        if self.cacheDuration > 0:
            return ViCareCachedServiceViaGateway(self.oauth_manager, self.cacheDuration)
        return ViCareServiceViaGateway(self.oauth_manager)

    def __loadInstallations(self):
        installations = self.oauth_manager.get(
            "/equipment/installations?includeGateways=true")
        if "data" not in installations:
            logger.error("Missing 'data' property when fetching installations")
            raise PyViCareInvalidDataError(installations)

        data = installations['data']
        self.installations = Wrap(data)
        self.all_devices = list(self.__extract_all_devices())
        self.devices = [d for d in self.all_devices
                        if d.device_type in self.SUPPORTED_DEVICE_TYPES]

    SUPPORTED_DEVICE_TYPES = [
        "heating", "zigbee", "vitoconnect", "electricityStorage",
        "tcu", "ventilation", "roomControl",
    ]

    def __extract_all_devices(self):
        for installation in self.installations:
            for gateway in installation.gateways:
                shared_service = self.__buildGatewayService() if self.viaGateway else None
                for device in gateway.devices:
                    accessor = ViCareDeviceAccessor(
                        installation.id, gateway.serial, device.id)
                    service = shared_service if shared_service is not None else self.__buildService(device.roles)

                    logger.info("Device found: %s (type=%s)", device.modelId, device.deviceType)

                    yield PyViCareDeviceConfig(accessor, service, device.modelId, device.status, device.deviceType, device.roles)


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
