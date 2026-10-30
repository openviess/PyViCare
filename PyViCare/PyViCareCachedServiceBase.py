import logging
import threading
from collections.abc import Callable
from datetime import date, datetime
from typing import Any, TypeVar, cast

from PyViCare.PyViCareEvent import ViCareEventPage
from PyViCare.PyViCareService import (
    ViCareDeviceAccessor,
    ViCareService,
    event_query_limit,
    format_query_date,
    format_query_datetime,
    readFeature,
)
from PyViCare.PyViCareUtils import (
    PyViCareDeviceCommunicationError,
    PyViCareInternalServerError,
    PyViCareInvalidDataError,
    PyViCareNotPaidForError,
    PyViCareNotSupportedFeatureError,
    ViCareTimer,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

_T = TypeVar("_T")


class _CacheSlot:
    """State of one cached payload."""

    def __init__(self) -> None:
        self.value: Any = None
        self.time: datetime | None = None
        self.error: Exception | None = None


class ViCareCachedServiceBase(ViCareService):
    """Time-based caching shared by the per-device and per-gateway services.

    Subclasses provide `_fetch_uncached` (the HTTP fetch) and `_extract_entities`
    (pick this device's features out of the cached payload).

    Features and events have separate cache slots: an event query depends on the
    event type and the window, so it cannot share the feature payload. Paging with
    a cursor is not cached, a cursor is used once.
    """

    def _init_cache(self, cacheDuration: int) -> None:
        self._cacheDuration = cacheDuration
        self._featureSlot = _CacheSlot()
        self._eventSlots: dict[tuple[Any, ...], _CacheSlot] = {}
        self._cacheLock = threading.Lock()

    def getProperty(self, accessor: ViCareDeviceAccessor, property_name: str) -> Any:
        data = self._get_or_update_cache(accessor)
        entities = self._extract_entities(data, accessor)
        return readFeature(entities, property_name)

    def fetch_all_features(self, accessor: ViCareDeviceAccessor) -> Any:
        # cached, so a caller refreshing with fetch_all_features() warms the
        # cache the following getProperty calls read from
        return self._get_or_update_cache(accessor)

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def fetch_events(self,
                     accessor: ViCareDeviceAccessor,
                     event_type: str | None = None,
                     last_days: int | None = None,
                     since: datetime | str | None = None,
                     on_date: date | datetime | str | None = None,
                     limit: int | None = None,
                     cursor: str | None = None) -> ViCareEventPage:
        def fetch() -> ViCareEventPage:
            return ViCareService.fetch_events(
                self, accessor, event_type, last_days, since, on_date, limit, cursor)

        if cursor is not None:
            # each cursor is used once, caching the pages would only keep them
            return fetch()

        key = (accessor.id, accessor.serial, event_type, last_days,
               format_query_datetime(since), format_query_date(on_date),
               event_query_limit(limit))
        return self._cached_events(key, fetch)

    def setProperty(self, accessor: ViCareDeviceAccessor, property_name: str, action: str, data: Any) -> Any:
        response = super().setProperty(accessor, property_name, action, data)
        self.clear_cache()
        return response

    def _get_or_update_cache(self, accessor: ViCareDeviceAccessor) -> Any:
        def fetch() -> Any:
            data = self._fetch_uncached(accessor)
            if "data" not in data:
                logger.error("Missing 'data' property when fetching data.")
                raise PyViCareInvalidDataError(data)
            return data

        return self._cached(self._featureSlot, fetch)

    def _cached_events(self, key: tuple[Any, ...], fetch: Callable[[], _T]) -> _T:
        with self._cacheLock:
            slot = self._eventSlots.setdefault(key, _CacheSlot())
            return cast(_T, self._read_slot(slot, fetch))

    def _cached(self, slot: _CacheSlot, fetch: Callable[[], _T]) -> _T:
        with self._cacheLock:
            return cast(_T, self._read_slot(slot, fetch))

    def _read_slot(self, slot: _CacheSlot, fetch: Callable[[], Any]) -> Any:
        # the caller holds _cacheLock
        if self._is_slot_invalid(slot):
            # we always set the cache time before we fetch the data
            # to avoid consuming all the api calls if the api is down
            # see https://github.com/home-assistant/core/issues/67052
            # we simply return the old cache in this case
            slot.time = ViCareTimer().now()
            slot.error = None

            try:
                slot.value = fetch()
            except PyViCareNotPaidForError as e:
                logger.error("Viessmann API denied access (PACKAGE_NOT_PAID_FOR). Features unavailable: %s", e)
                if slot.value is not None:
                    return slot.value
                slot.error = PyViCareNotSupportedFeatureError("PACKAGE_NOT_PAID_FOR")
                raise slot.error
            except (PyViCareDeviceCommunicationError, PyViCareInternalServerError) as e:
                if slot.value is not None:
                    logger.warning("API error, returning stale cache: %s", e)
                    return slot.value
                slot.error = e
                raise
            except Exception as e:
                slot.error = e
                raise
        elif slot.value is None and slot.error is not None:
            # The fetch that opened this window failed and left nothing to
            # read. Replaying its error keeps every other reader from
            # spending a request of its own before the window is over. The
            # traceback is dropped because the instance is shared.
            raise slot.error.with_traceback(None) from None
        return slot.value

    def is_cache_invalid(self) -> bool:
        return self._is_slot_invalid(self._featureSlot)

    def _is_slot_invalid(self, slot: _CacheSlot) -> bool:
        return slot.time is None or (ViCareTimer().now() - slot.time).seconds > self._cacheDuration

    def clear_cache(self):
        with self._cacheLock:
            self._featureSlot = _CacheSlot()
            self._eventSlots.clear()

    def _fetch_uncached(self, accessor: ViCareDeviceAccessor) -> Any:
        raise NotImplementedError

    def _extract_entities(self, data: dict, accessor: ViCareDeviceAccessor) -> list[dict[str, Any]]:
        raise NotImplementedError
