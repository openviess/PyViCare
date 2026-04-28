import logging
from datetime import datetime

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareBrowserOAuthManager import ViCareBrowserOAuthManager
from PyViCare.PyViCareCachedService import ViCareCachedService
from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareOAuthManager import ViCareOAuthManager
from PyViCare.PyViCareRoomControl import RoomControl
from PyViCare.PyViCareService import ViCareDeviceAccessor, ViCareService
from PyViCare.PyViCareUtils import PyViCareInvalidDataError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PyViCare:
    """"Viessmann ViCare API Python tools"""
    def __init__(self) -> None:
        self.cacheDuration = 60

    def setCacheDuration(self, cache_duration):
        self.cacheDuration = int(cache_duration)

    def initWithCredentials(self, username: str, password: str, client_id: str, token_file: str):
        self.initWithExternalOAuth(ViCareOAuthManager(
            username, password, client_id, token_file))

    def initWithExternalOAuth(self, oauth_manager: AbstractViCareOAuthManager) -> None:
        self.oauth_manager = oauth_manager
        self.__loadInstallations()

    def initWithBrowserOAuth(self, client_id: str, token_file: str) -> None:
        self.initWithExternalOAuth(ViCareBrowserOAuthManager(client_id, token_file))

    def __buildService(self, accessor, roles):
        if self.cacheDuration > 0:
            return ViCareCachedService(self.oauth_manager, accessor, roles, self.cacheDuration)
        return ViCareService(self.oauth_manager, accessor, roles)

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
        self.__enrichZigbeeDevices()

    SUPPORTED_DEVICE_TYPES = [
        "heating", "zigbee", "vitoconnect", "electricityStorage",
        "tcu", "ventilation", "roomControl",
    ]

    def __extract_all_devices(self):
        for installation in self.installations:
            for gateway in installation.gateways:
                for device in gateway.devices:
                    accessor = ViCareDeviceAccessor(
                        installation.id, gateway.serial, device.id)
                    service = self.__buildService(accessor, device.roles)

                    logger.info("Device found: %s (type=%s)", device.modelId, device.deviceType)

                    yield PyViCareDeviceConfig(service, device.id, device.modelId, device.status, device.deviceType, device.roles)

    def __enrichZigbeeDevices(self):
        """Enrich Zigbee devices with sensor data from RoomControl.

        Viessmann moved temperature/humidity data from physical Zigbee
        sensors to the RoomControl virtual device. This reverses that
        mapping by cross-referencing RoomControl actors with Zigbee
        device IDs.
        """
        devices_by_id = {device_config.device_id: device_config for device_config in self.devices}

        for device_config in self.devices:
            if device_config.device_type != "roomControl":
                continue

            room_control = RoomControl(device_config.service)
            try:
                actor_map = room_control.buildActorRoomMap()
            except Exception:
                logger.debug("Could not build actor map for %s", device_config.getModel(), exc_info=True)
                continue

            for device_id, room_id in actor_map.items():
                zigbee_config = devices_by_id.get(device_id)
                if zigbee_config is None:
                    continue
                zigbee_config.setRoomControlEnrichment(room_control, room_id)
                logger.info("Enriched %s with room %s data from %s",
                            zigbee_config.device_id, room_id, device_config.getModel())


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
