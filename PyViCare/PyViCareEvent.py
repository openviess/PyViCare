"""Events from the Viessmann event history.

The event history keeps past device errors. The ``device.messages.errors.raw``
feature is missing on some gateways, and ``heating.burners.0.errorStatus`` only
holds the current value.

A device error appears as two events: one with ``active`` set to True when the
fault was raised, one with ``active`` set to False when it was cleared. The
newest event of an error code tells you whether that error still stands.
"""

from datetime import datetime
from typing import Any

EVENT_TYPE_DEVICE_ERROR = "device-error"

# The API does not validate event types: an unknown value returns an empty list
# instead of an error, and values are matched exactly (case sensitive). A name
# can therefore only be confirmed by an installation that reports such events.
#
# Observed on other installations (unverified against the current API version):
#   device-message-status   status messages   (S.x codes)
#   device-message-info     information       (I.x codes)
#   device-message-warning  alarms            (A.x codes)
#   feature-changed         setting changes
#   gateway-online, gateway-reset-command
# The event type for maintenance messages (P.x) is unknown.
#
# Several values can be combined with commas, the API ORs them.


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_str(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _as_bool(value: Any) -> bool:
    return value is True


def _as_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


class ViCareEvent:
    """One entry of the event history."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, raw: dict[str, Any]) -> None:
        body = _as_dict(raw.get("body"))

        self.raw = raw
        self.event_type = _as_str(raw.get("eventType")) or ""
        self.gateway_serial = _as_str(raw.get("gatewaySerial"))
        self.device_id = _as_str(body.get("deviceId"))
        self.error_code = _as_str(body.get("errorCode"))
        self.error_description = _as_str(body.get("errorDescription"))
        self.error_event_type = _as_str(body.get("errorEventType"))
        self.equipment_type = _as_str(body.get("equipmentType"))
        self.model_id = _as_str(body.get("modelId"))
        self.active = _as_bool(body.get("active"))
        self.event_timestamp = _as_datetime(raw.get("eventTimestamp"))
        self.created_at = _as_datetime(raw.get("createdAt"))
        self.origin = _as_str(raw.get("origin"))

    def __repr__(self) -> str:
        return (
            f"ViCareEvent({self.event_type}, error={self.error_code}, "
            f"active={self.active}, at={self.event_timestamp})"
        )


class ViCareEventPage:
    """One page of the event history, with the cursor for the next page."""

    def __init__(self, events: list[ViCareEvent], next_cursor: str | None, raw: dict[str, Any]) -> None:
        self.events = events
        self.next_cursor = next_cursor
        self.raw = raw

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "ViCareEventPage":
        data = payload.get("data")
        entries = data if isinstance(data, list) else []
        events = [ViCareEvent(entry) for entry in entries if isinstance(entry, dict)]
        cursor = _as_str(_as_dict(payload.get("cursor")).get("next")) or None
        return cls(events, cursor, payload)

    def __repr__(self) -> str:
        return f"ViCareEventPage({len(self.events)} events, next={self.next_cursor!r})"
