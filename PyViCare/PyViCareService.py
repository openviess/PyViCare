import json
import logging
from typing import Any, List

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def readFeature(entities, property_name):
    feature = next(
        (f for f in entities if f["feature"] == property_name), None)

    if feature is None:
        raise PyViCareNotSupportedFeatureError(property_name)

    return feature

def hasRoles(requested_roles: List[str], existing_roles: List[str]) -> bool:
    return len(requested_roles) > 0 and set(requested_roles).issubset(set(existing_roles))

GATEWAY_ROLES = [
    "type:gateway;VitoconnectOpto1",
    "type:gateway;VitoconnectOpto2/OT2",
    "type:gateway;TCU100",
    "type:gateway;TCU200",
    "type:gateway;TCU300",
]

def is_gateway_role(roles: List[str]) -> bool:
    return any(hasRoles([role], roles) for role in GATEWAY_ROLES)

def buildSetPropertyUrl(accessor, property_name, action):
    return f'/features/installations/{accessor.id}/gateways/{accessor.serial}/devices/{accessor.device_id}/features/{property_name}/commands/{action}'

class ViCareDeviceAccessor:
    def __init__(self, _id: int, serial: str, device_id: str) -> None:
        self.id = _id
        self.serial = serial
        self.device_id = device_id

class ViCareService:
    def __init__(self, oauth_manager: AbstractViCareOAuthManager, roles: List[str]) -> None:
        self.oauth_manager = oauth_manager
        self.roles = roles

    def getProperty(self, accessor: ViCareDeviceAccessor, property_name: str) -> Any:
        url = self.buildGetPropertyUrl(accessor, property_name)
        return self.oauth_manager.get(url)

    def buildGetPropertyUrl(self, accessor: ViCareDeviceAccessor, property_name):
        if is_gateway_role(self.roles):
            return f'/features/installations/{accessor.id}/gateways/{accessor.serial}/features/{property_name}'
        return f'/features/installations/{accessor.id}/gateways/{accessor.serial}/devices/{accessor.device_id}/features/{property_name}'

    def hasRoles(self, requested_roles) -> bool:
        return hasRoles(requested_roles, self.roles)

    def setProperty(self, accessor: ViCareDeviceAccessor, property_name: str, action: str, data: Any) -> Any:
        url = buildSetPropertyUrl(accessor, property_name, action)

        post_data = data if isinstance(data, str) else json.dumps(data)
        return self.oauth_manager.post(url, post_data)

    def fetch_all_features(self, accessor: ViCareDeviceAccessor) -> Any:
        url = f'/features/installations/{accessor.id}/gateways/{accessor.serial}/devices/{accessor.device_id}/features/'
        if is_gateway_role(self.roles):
            url = f'/features/installations/{accessor.id}/gateways/{accessor.serial}/features/'
        return self.oauth_manager.get(url)

    def reboot_gateway(self, accessor: ViCareDeviceAccessor) -> Any:
        url = f'/equipment/installations/{accessor.id}/gateways/{accessor.serial}/reboot'
        data = "{}"
        return self.oauth_manager.post(url, data)
