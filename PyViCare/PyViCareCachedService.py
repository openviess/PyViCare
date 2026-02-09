import logging
import threading
from typing import Any, List

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareService import (ViCareDeviceAccessor, ViCareService,
                                      readFeature)
from PyViCare.PyViCareUtils import (PyViCareDeviceCommunicationError,
                                    PyViCareInvalidDataError,
                                    PyViCareInternalServerError,
                                    ViCareTimer)

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())


class ViCareCachedService(ViCareService):

    def __init__(self, oauth_manager: AbstractViCareOAuthManager, accessor: ViCareDeviceAccessor, roles: List[str], cacheDuration: int) -> None:
        ViCareService.__init__(self, oauth_manager, accessor, roles)
        self.__cacheDuration = cacheDuration
        self.__cache = None
        self.__cacheTime = None
        self.__lock = threading.Lock()

    def getProperty(self, property_name: str) -> Any:
        data = self.__get_or_update_cache()
        entities = data["data"]
        return readFeature(entities, property_name)

    def setProperty(self, property_name, action, data):
        response = super().setProperty(property_name, action, data)
        self.clear_cache()
        return response

    def __get_or_update_cache(self):
        with self.__lock:
            if self.is_cache_invalid():
                # we always set the cache time before we fetch the data
                # to avoid consuming all the api calls if the api is down
                # see https://github.com/home-assistant/core/issues/67052
                # we simply return the old cache in this case
                self.__cacheTime = ViCareTimer().now()

                try:
                    data = self.fetch_all_features()
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
