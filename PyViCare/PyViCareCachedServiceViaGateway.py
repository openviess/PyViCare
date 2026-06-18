import logging
import threading
from datetime import datetime
from typing import Any, Optional

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareService import ViCareDeviceAccessor, readFeature
from PyViCare.PyViCareServiceViaGateway import (
    ViCareServiceViaGateway, filter_features_for_device)
from PyViCare.PyViCareUtils import (PyViCareDeviceCommunicationError,
                                    PyViCareInternalServerError,
                                    PyViCareInvalidDataError,
                                    PyViCareNotPaidForError,
                                    PyViCareNotSupportedFeatureError,
                                    ViCareTimer)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ViCareCachedServiceViaGateway(ViCareServiceViaGateway):
    """Cached variant of the gateway bulk-fetch service.

    A single instance is shared across all devices on the gateway. The bulk
    response is cached once per (oauth, gateway) and every device's
    getProperty reads from the same cached payload. setProperty invalidates
    the whole cache because writes can affect any feature on any device.
    """

    def __init__(self, oauth_manager: AbstractViCareOAuthManager, cacheDuration: int) -> None:
        ViCareServiceViaGateway.__init__(self, oauth_manager)
        self.__cacheDuration = cacheDuration
        self.__cache: Optional[dict] = None
        self.__cacheTime: Optional[datetime] = None
        self.__lock = threading.Lock()

    def getProperty(self, accessor: ViCareDeviceAccessor, property_name: str) -> Any:
        data = self.__get_or_update_cache(accessor)
        entities = filter_features_for_device(data["data"], accessor.device_id)
        return readFeature(entities, property_name)

    def fetch_all_features(self, accessor: ViCareDeviceAccessor) -> Any:
        # Cached too: in gateway mode there is exactly one bulk endpoint per
        # gateway, so concurrent fetch_all_features() callers (e.g. one
        # DataUpdateCoordinator per device) all consume the same response.
        # Returning the cached payload here is the only way the shared
        # service actually delivers the API-call savings.
        return self.__get_or_update_cache(accessor)

    def setProperty(self, accessor: ViCareDeviceAccessor, property_name: str, action: str, data: Any) -> Any:
        response = super().setProperty(accessor, property_name, action, data)
        self.clear_cache()
        return response

    def _fetch_bulk_uncached(self, accessor: ViCareDeviceAccessor) -> Any:
        return super().fetch_all_features(accessor)

    def __get_or_update_cache(self, accessor: ViCareDeviceAccessor):
        with self.__lock:
            if self.is_cache_invalid():
                # we always set the cache time before we fetch the data
                # to avoid consuming all the api calls if the api is down
                # see https://github.com/home-assistant/core/issues/67052
                # we simply return the old cache in this case
                self.__cacheTime = ViCareTimer().now()

                try:
                    data = self._fetch_bulk_uncached(accessor)
                except PyViCareNotPaidForError as e:
                    logger.error("Viessmann API denied access (PACKAGE_NOT_PAID_FOR). Features unavailable: %s", e)
                    if self.__cache is not None:
                        return self.__cache
                    raise PyViCareNotSupportedFeatureError("PACKAGE_NOT_PAID_FOR")
                except (PyViCareDeviceCommunicationError, PyViCareInternalServerError) as e:
                    if self.__cache is not None:
                        logger.warning("API error, returning stale cache: %s", e)
                        return self.__cache
                    raise

                if "data" not in data:
                    logger.error("Missing 'data' property when fetching data.")
                    raise PyViCareInvalidDataError(data)
                self.__cache = data
            return self.__cache

    def is_cache_invalid(self) -> bool:
        return self.__cache is None or self.__cacheTime is None or (ViCareTimer().now() - self.__cacheTime).seconds > self.__cacheDuration

    def clear_cache(self):
        with self.__lock:
            self.__cache = None
            self.__cacheTime = None
