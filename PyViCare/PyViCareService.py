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

_MAX_EVENT_LIMIT = 1000

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


def _format_query_datetime(value: datetime | None) -> str | None:
    """Format a datetime as the ISO 8601 UTC string the API expects.

    Naive datetimes are read as UTC.
    """
    if value is None:
        return None

    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


def _format_query_date(value: date | None) -> str | None:
    """Format a date as the ISO 8601 date the API expects."""
    if value is None:
        return None

    if isinstance(value, datetime):
        raise TypeError("on_date takes a datetime.date, not datetime.datetime")
    return value.isoformat()


def _event_query_limit(limit: int | None) -> int | None:
    """Clamp the page size to what the API accepts (1000)."""
    if limit is None:
        return None

    if limit < 1:
        raise ValueError("limit must be 1 or more")
    return min(limit, _MAX_EVENT_LIMIT)


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
        response = self.oauth_manager.get(url)
        # A missing feature comes back as a 404 body, not as an exception.
        if "data" not in response:
            raise PyViCareNotSupportedFeatureError(property_name)
        return response["data"]

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

    # pylint: disable=too-many-arguments
    def _build_events_url(self,
                          accessor: ViCareDeviceAccessor,
                          event_type: str | None = None,
                          *,
                          last_days: int | None = None,
                          since: datetime | None = None,
                          on_date: date | None = None,
                          gateway_serials: str | None = None,
                          limit: int | None = None,
                          cursor: str | None = None) -> str:
        if sum(window is not None for window in (last_days, since, on_date)) > 1:
            raise ValueError("last_days, since and on_date cannot be combined")
        if last_days is not None and last_days < 1:
            raise ValueError("last_days must be 1 or more")

        params = {
            'eventType': event_type,
            'lastNDays': last_days,
            'timestamp': _format_query_datetime(since),
            'date': _format_query_date(on_date),
            'gatewaySerials': gateway_serials,
            'limit': _event_query_limit(limit),
            'cursor': cursor,
        }
        # the cursor is base64 and the timestamps contain colons, so encode them
        query = urlencode({key: value for key, value in params.items() if value is not None})
        url = f'/events-history/installations/{accessor.id}/events'
        return f'{url}?{query}' if query else url

    # pylint: disable=too-many-arguments
    def fetch_events(self,
                     accessor: ViCareDeviceAccessor,
                     event_type: str | None = None,
                     *,
                     last_days: int | None = None,
                     since: datetime | None = None,
                     on_date: date | None = None,
                     gateway_serials: str | None = None,
                     limit: int | None = None,
                     cursor: str | None = None) -> ViCareEventPage:
        """Events of the installation this accessor belongs to.

        The API returns them newest ingestion first, so a late arriving event
        can precede an older one. Compare `event_timestamp` when the chronology
        matters.

        The API filters by `event_type`, `gateway_serials` (comma separated),
        one time window and the page size; the device id is not a parameter and
        is filtered by the caller. Pass the `next_cursor` of a page as `cursor`
        to fetch the following one.

        The time window is `last_days`, `since` (from that instant until now)
        or `on_date` (events of one day). Only one of them may be given, the
        API rejects combinations. `limit` defaults to 50 on the server, values
        above 1000 are clamped, values below 1 raise ValueError.

        `event_type` is matched exactly and is not validated; several values
        such as "device-error,device-message-warning" are OR-ed by the API.
        """
        url = self._build_events_url(
            accessor, event_type, last_days=last_days, since=since, on_date=on_date,
            gateway_serials=gateway_serials, limit=limit, cursor=cursor)
        response = self.oauth_manager.get(url)

        if not isinstance(response, dict) or 'data' not in response:
            logger.error("Missing 'data' property when fetching events.")
            raise PyViCareInvalidDataError(response)

        return ViCareEventPage.from_payload(response)
