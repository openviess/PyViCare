"""Device errors derived from the event history.

The event history returns device errors as raise and clear events, newest
first, one page at a time. ``ViCareErrorHistory`` turns successive pages into
the events that are new since the previous page and the errors that stand,
and can save its state so a restart neither repeats nor loses events.
"""

from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from PyViCare.PyViCareEvent import ViCareEvent

# device id, error code, active, time of the event
_EventKey = tuple[str, str, bool, str]
# device id, error code
_ErrorKey = tuple[str, str]

_NO_TIME = datetime.min.replace(tzinfo=UTC)


def _time(event: ViCareEvent) -> datetime:
    return event.event_timestamp or event.created_at or _NO_TIME


def chronological(events: Iterable[ViCareEvent]) -> list[ViCareEvent]:
    """Order events oldest first.

    The API returns them newest first. Events of the same time keep the order
    they happened in, so a raise and the clear of the same second stay in
    that order. ``createdAt`` stands in for a missing ``eventTimestamp``.
    """
    # sorted() is stable: oldest arrival first among events of the same time
    oldest_arrival_first = list(events)
    oldest_arrival_first.reverse()
    return sorted(oldest_arrival_first, key=_time)


def _event_key(event: ViCareEvent) -> _EventKey | None:
    if not event.device_id or not event.error_code:
        return None
    return (event.device_id, event.error_code, event.active, _time(event).isoformat())


def _is_event_key(value: Any) -> bool:
    return (isinstance(value, list) and len(value) == 4
            and isinstance(value[0], str) and isinstance(value[1], str)
            and isinstance(value[2], bool) and isinstance(value[3], str))


class ViCareErrorHistory:
    """Track the device errors of one gateway across fetches of the history.

    Pass each page of ``device-error`` events, as the API returns it, to
    ``update()``. The first page is the past: nothing in it is new. An error
    whose raise drops off the end of the page still stands until its clear
    arrives.
    """

    def __init__(self) -> None:
        self._seen: set[_EventKey] | None = None
        self._standing: dict[_ErrorKey, ViCareEvent] = {}

    @property
    def initialized(self) -> bool:
        """Whether a page was seen, here or before the state was saved."""
        return self._seen is not None

    def update(self, events: Iterable[ViCareEvent]) -> list[ViCareEvent]:
        """Take the newest page of events and return the new ones, oldest first.

        An event is new when it was not on the previous page. The page always
        holds the newest events, so an event that dropped off its end does not
        come back.
        """
        keyed = [(key, event) for event in chronological(events)
                 if (key := _event_key(event)) is not None]

        newest: dict[_ErrorKey, ViCareEvent] = {}
        for (device_id, error_code, _, _), event in keyed:
            newest[(device_id, error_code)] = event
        for error, event in newest.items():
            if event.active:
                self._standing[error] = event
            else:
                self._standing.pop(error, None)

        seen = self._seen
        self._seen = {key for key, _ in keyed}
        if seen is None:
            return []
        return [event for key, event in keyed if key not in seen]

    def active_errors(self, device_id: str) -> list[ViCareEvent]:
        """Return the raises of the errors of the device that stand, oldest first."""
        return sorted(
            (event for (device, _), event in self._standing.items() if device == device_id),
            key=_time)

    def as_dict(self) -> dict[str, Any]:
        """Return the state, JSON serializable, for ``from_dict()``."""
        return {
            'seen': None if self._seen is None else [list(key) for key in sorted(self._seen)],
            'standing': [event.raw for event in self._standing.values()],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'ViCareErrorHistory':
        """Restore the state from ``as_dict()``. Unreadable state starts over."""
        history = cls()
        seen = data.get('seen')
        standing = data.get('standing')
        if not isinstance(seen, list) or not all(_is_event_key(key) for key in seen):
            return history
        if not isinstance(standing, list) or not all(isinstance(raw, dict) for raw in standing):
            return history
        history._seen = {(key[0], key[1], key[2], key[3]) for key in seen}
        for event in (ViCareEvent(raw) for raw in standing):
            if event.device_id and event.error_code and event.active:
                history._standing[(event.device_id, event.error_code)] = event
        return history
