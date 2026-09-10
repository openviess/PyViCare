import logging
import threading
from datetime import datetime
from typing import Any, Optional

from PyViCare.PyViCareService import (ViCareDeviceAccessor, ViCareService,
                                      readFeature)
from PyViCare.PyViCareUtils import (PyViCareDeviceCommunicationError,
                                    PyViCareInternalServerError,
                                    PyViCareInvalidDataError,
                                    PyViCareNotPaidForError,
                                    PyViCareNotSupportedFeatureError,
                                    ViCareTimer)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ViCareCachedServiceBase(ViCareService):
    """Time-based caching shared by the per-device and per-gateway services.

    Subclasses provide `_fetch_uncached` (the HTTP fetch) and `_extract_entities`
    (pick this device's features out of the cached payload).
    """

    def _init_cache(self, cacheDuration: int) -> None:
        self._cacheDuration = cacheDuration
        self._cache: Optional[dict] = None
        self._cacheTime: Optional[datetime] = None
        self._cacheError: Optional[Exception] = None
        self._cacheLock = threading.Lock()

    def getProperty(self, accessor: ViCareDeviceAccessor, property_name: str) -> Any:
        data = self._get_or_update_cache(accessor)
        entities = self._extract_entities(data, accessor)
        return readFeature(entities, property_name)

    def fetch_all_features(self, accessor: ViCareDeviceAccessor) -> Any:
        # cached, so a caller refreshing with fetch_all_features() warms the
        # cache the following getProperty calls read from
        return self._get_or_update_cache(accessor)

    def setProperty(self, accessor: ViCareDeviceAccessor, property_name: str, action: str, data: Any) -> Any:
        response = super().setProperty(accessor, property_name, action, data)
        self.clear_cache()
        return response

    def _get_or_update_cache(self, accessor: ViCareDeviceAccessor):
        with self._cacheLock:
            if self.is_cache_invalid():
                # we always set the cache time before we fetch the data
                # to avoid consuming all the api calls if the api is down
                # see https://github.com/home-assistant/core/issues/67052
                # we simply return the old cache in this case
                self._cacheTime = ViCareTimer().now()
                self._cacheError = None

                try:
                    data = self._fetch_uncached(accessor)
                    if "data" not in data:
                        logger.error("Missing 'data' property when fetching data.")
                        raise PyViCareInvalidDataError(data)
                except PyViCareNotPaidForError as e:
                    logger.error("Viessmann API denied access (PACKAGE_NOT_PAID_FOR). Features unavailable: %s", e)
                    if self._cache is not None:
                        return self._cache
                    self._cacheError = PyViCareNotSupportedFeatureError("PACKAGE_NOT_PAID_FOR")
                    raise self._cacheError
                except (PyViCareDeviceCommunicationError, PyViCareInternalServerError) as e:
                    if self._cache is not None:
                        logger.warning("API error, returning stale cache: %s", e)
                        return self._cache
                    self._cacheError = e
                    raise
                except Exception as e:
                    self._cacheError = e
                    raise

                self._cache = data
            elif self._cache is None and self._cacheError is not None:
                # The fetch that opened this window failed and left nothing to
                # read. Replaying its error keeps every other reader from
                # spending a request of its own before the window is over. The
                # traceback is dropped because the instance is shared.
                raise self._cacheError.with_traceback(None) from None
            return self._cache

    def is_cache_invalid(self) -> bool:
        return self._cacheTime is None or (ViCareTimer().now() - self._cacheTime).seconds > self._cacheDuration

    def clear_cache(self):
        with self._cacheLock:
            self._cache = None
            self._cacheTime = None
            self._cacheError = None

    def _fetch_uncached(self, accessor: ViCareDeviceAccessor) -> Any:
        raise NotImplementedError

    def _extract_entities(self, data: dict, accessor: ViCareDeviceAccessor) -> list[dict[str, Any]]:
        raise NotImplementedError
