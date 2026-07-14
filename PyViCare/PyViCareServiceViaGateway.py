import logging
from typing import Any

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareService import (ViCareDeviceAccessor, ViCareService,
                                      readFeature)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def filter_features_for_device(entities: list[dict[str, Any]], device_id: str) -> list[dict[str, Any]]:
    device_segment = f"/devices/{device_id}/"
    return [e for e in entities if device_segment in e.get("uri", "")]


class ViCareServiceViaGateway(ViCareService):
    """Service that reads all device features from the gateway-wide bulk endpoint.

    One instance can serve multiple devices on the same gateway: the bulk
    response contains features for all devices, and getProperty filters by
    accessor.device_id at read time.
    """

    def __init__(self, oauth_manager: AbstractViCareOAuthManager) -> None:
        ViCareService.__init__(self, oauth_manager, [])

    def getProperty(self, accessor: ViCareDeviceAccessor, property_name: str) -> Any:
        data = self.fetch_all_features(accessor)
        entities = filter_features_for_device(data["data"], accessor.device_id)
        return readFeature(entities, property_name)

    def fetch_all_features(self, accessor: ViCareDeviceAccessor) -> Any:
        url = (
            f'/features/installations/{accessor.id}'
            f'/gateways/{accessor.serial}/features?includeDevicesFeatures=true'
        )
        return self.oauth_manager.get(url)
