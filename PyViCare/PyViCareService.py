import json
import logging
from datetime import UTC, date, datetime
from typing import Any
from urllib.parse import urlencode

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareEvent import ViCareEventPage
from PyViCare.PyViCareUtils import (
    PyViCareInvalidDataError,
    PyViCareNotSupportedFeatureError,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def readFeature(entities, property_name):
    feature = next(
        (f for f in entities if f["feature"] == property_name), None)

    if feature is None:
        raise PyViCareNotSupportedFeatureError(property_name)

    return feature

def hasRoles(requested_roles: list[str], existing_roles: list[str]) -> bool:
    return len(requested_roles) > 0 and set(requested_roles).issubset(set(existing_roles))

MAX_EVENT_LIMIT = 1000

GATEWAY_ROLES = [
    "type:gateway;VitoconnectOpto1",
    "type:gateway;VitoconnectOpto2/OT2",
    "type:gateway;TCU100",
    "type:gateway;TCU200",
    "type:gateway;TCU300",
]

def is_gateway_role(roles: list[str]) -> bool:
    return any(hasRoles([role], roles) for role in GATEWAY_ROLES)

def buildSetPropertyUrl(accessor, property_name, action):
    return f'/features/installations/{accessor.id}/gateways/{accessor.serial}/devices/{accessor.device_id}/features/{property_name}/commands/{action}'


def format_query_datetime(value: datetime | str | None) -> str | None:
    """Format a datetime as the ISO 8601 UTC string the API expects.

    Strings pass through unchanged, naive datetimes are read as UTC.
    """
    if value is None or isinstance(value, str):
        return value

    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


def format_query_date(value: date | datetime | str | None) -> str | None:
    """Format a date or datetime as the ISO 8601 date the API expects."""
    if value is None or isinstance(value, str):
        return value

    if isinstance(value, datetime):
        value = value.date()
    return value.isoformat()


def event_query_limit(limit: int | None) -> int | None:
    """Clamp the page size to what the API accepts (1000), 0 means no limit."""
    if limit is None:
        return None

    limit = min(int(limit), MAX_EVENT_LIMIT)
    return limit if limit > 0 else None

class ViCareDeviceAccessor:
    def __init__(self, _id: int, serial: str, device_id: str) -> None:
        self.id = _id
        self.serial = serial
        self.device_id = device_id

class ViCareService:
    def __init__(self, oauth_manager: AbstractViCareOAuthManager, roles: list[str]) -> None:
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

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def build_events_url(self,
                         accessor: ViCareDeviceAccessor,
                         event_type: str | None = None,
                         last_days: int | None = None,
                         since: datetime | str | None = None,
                         on_date: date | datetime | str | None = None,
                         limit: int | None = None,
                         cursor: str | None = None) -> str:
        if sum(window is not None for window in (last_days, since, on_date)) > 1:
            raise ValueError("last_days, since and on_date cannot be combined")
        if last_days is not None and last_days < 1:
            raise ValueError("last_days must be 1 or more")

        params = {
            'eventType': event_type,
            'lastNDays': last_days,
            'timestamp': format_query_datetime(since),
            'date': format_query_date(on_date),
            'limit': event_query_limit(limit),
            'cursor': cursor,
        }
        # the cursor is base64 and the timestamps contain colons, so encode them
        query = urlencode({key: value for key, value in params.items() if value is not None})
        url = f'/events-history/installations/{accessor.id}/events'
        return f'{url}?{query}' if query else url

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def fetch_events(self,
                     accessor: ViCareDeviceAccessor,
                     event_type: str | None = None,
                     last_days: int | None = None,
                     since: datetime | str | None = None,
                     on_date: date | datetime | str | None = None,
                     limit: int | None = None,
                     cursor: str | None = None) -> ViCareEventPage:
        """Events of the installation this accessor belongs to, newest first.

        The event history is per installation, not per device, so `eventType`
        is the only server-side filter. Pass the `next_cursor` of a page as
        `cursor` to fetch the following one.

        The time window is `last_days`, `since` (from that instant until now)
        or `on_date` (events of one day). Only one of them may be given, the
        API rejects combinations. `limit` is capped at the API maximum of 1000.

        `event_type` is matched exactly and is not validated; several values
        such as "device-error,device-message-warning" are OR-ed by the API.
        """
        url = self.build_events_url(accessor, event_type, last_days, since, on_date, limit, cursor)
        response = self.oauth_manager.get(url)

        if not isinstance(response, dict) or 'data' not in response:
            logger.error("Missing 'data' property when fetching events.")
            raise PyViCareInvalidDataError(response)

        return ViCareEventPage.from_payload(response)
