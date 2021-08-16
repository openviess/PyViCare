import json
import logging
from typing import Any

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())


def readFeature(entities, property_name):
    feature = next(
        (f for f in entities if f["feature"] == property_name), None)

    if(feature is None):
        raise PyViCareNotSupportedFeatureError(property_name)

    return feature


def buildSetPropertyUrl(accessor, property_name, action):
    return f'/equipment/installations/{accessor.id}/gateways/{accessor.serial}/devices/{accessor.device_id}/features/{property_name}/{action}'


def buildGetPropertyUrl(accessor, property_name):
    return f'/equipment/installations/{accessor.id}/gateways/{accessor.serial}/devices/{accessor.device_id}/features/{property_name}'


class ViCareDeviceAccessor:
    def __init__(self, id: int, serial: str, device_id: str) -> None:
        self.id = id
        self.serial = serial
        self.device_id = device_id


class ViCareService:
    def __init__(self, oauth_manager: AbstractViCareOAuthManager, accessor: ViCareDeviceAccessor) -> None:
        self.oauth_manager = oauth_manager
        self.accessor = accessor

    def getProperty(self, property_name: str) -> Any:
        url = buildGetPropertyUrl(
            self.accessor, property_name)
        return self.oauth_manager.get(url)

    def setProperty(self, property_name: str, action: str, data: Any) -> Any:
        url = buildSetPropertyUrl(
            self.accessor, property_name, action)

        post_data = data if isinstance(data, str) else json.dumps(data)
        return self.oauth_manager.post(url, post_data)

    def fetch_all_features(self) -> Any:
        url = f'/equipment/installations/{self.accessor.id}/gateways/{self.accessor.serial}/devices/{self.accessor.device_id}/features/'
        return self.oauth_manager.get(url)
