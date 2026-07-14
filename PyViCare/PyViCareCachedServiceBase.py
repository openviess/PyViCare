import logging
import threading
from datetime import datetime
from typing import Any, Optional

from PyViCare.PyViCareService import ViCareDeviceAccessor, readFeature
from PyViCare.PyViCareUtils import (PyViCareDeviceCommunicationError,
                                    PyViCareInternalServerError,
                                    PyViCareInvalidDataError,
                                    PyViCareNotPaidForError,
                                    PyViCareNotSupportedFeatureError,
                                    ViCareTimer)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ViCareCachedServiceBase:
    """Time-based caching shared by the per-device and per-gateway services.

    Subclasses provide `_fetch_uncached` (the HTTP fetch) and `_extract_entities`
    (pick this device's features out of the cached payload).
    """

    def _init_cache(self, cacheDuration: int) -> None:
        self._cacheDuration = cacheDuration
        self._cache: Optional[dict] = None
        self._cacheTime: Optional[datetime] = None
        self._cacheLock = threading.Lock()

    def getProperty(self, accessor: ViCareDeviceAccessor, property_name: str) -> Any:
        data = self._get_or_update_cache(accessor)
        entities = self._extract_entities(data, accessor)
        return readFeature(entities, property_name)

    def setProperty(self, accessor: ViCareDeviceAccessor, property_name: str, action: str, data: Any) -> Any:
        # super() -> concrete service via MRO
        response = super().setProperty(accessor, property_name, action, data)  # type: ignore[misc]
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

                try:
                    data = self._fetch_uncached(accessor)
                except PyViCareNotPaidForError as e:
                    logger.error("Viessmann API denied access (PACKAGE_NOT_PAID_FOR). Features unavailable: %s", e)
                    if self._cache is not None:
                        return self._cache
                    raise PyViCareNotSupportedFeatureError("PACKAGE_NOT_PAID_FOR")
                except (PyViCareDeviceCommunicationError, PyViCareInternalServerError) as e:
                    if self._cache is not None:
                        logger.warning("API error, returning stale cache: %s", e)
                        return self._cache
                    raise

                if "data" not in data:
                    logger.error("Missing 'data' property when fetching data.")
                    raise PyViCareInvalidDataError(data)
                self._cache = data
            return self._cache

    def is_cache_invalid(self) -> bool:
        return self._cache is None or self._cacheTime is None or (ViCareTimer().now() - self._cacheTime).seconds > self._cacheDuration

    def clear_cache(self):
        with self._cacheLock:
            self._cache = None
            self._cacheTime = None

    def _fetch_uncached(self, accessor: ViCareDeviceAccessor) -> Any:
        raise NotImplementedError

    def _extract_entities(self, data: dict, accessor: ViCareDeviceAccessor) -> list[dict[str, Any]]:
        raise NotImplementedError
