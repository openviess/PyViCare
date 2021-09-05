import logging
import threading
from datetime import datetime
from typing import Any

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareService import (ViCareDeviceAccessor, ViCareService,
                                      readFeature)
from PyViCare.PyViCareUtils import PyViCareInvalidDataError

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())


class ViCareTimer:
    # class is used to replace logic in unittest
    def now(self) -> datetime:
        return datetime.now()


class ViCareCachedService(ViCareService):

    def __init__(self, oauth_manager: AbstractViCareOAuthManager, accessor: ViCareDeviceAccessor, cacheDuration: int) -> None:
        ViCareService.__init__(self, oauth_manager, accessor)
        self.__cacheDuration = cacheDuration
        self.__cache = None
        self.__cacheTime = None
        self.__lock = threading.Lock()

    def getProperty(self, property_name: str) -> Any:
        data = self.__get_or_update_cache()

        if "data" not in data:
            logger.error("Missing 'data' property when fetching data.")
            raise PyViCareInvalidDataError(data)

        entities = data["data"]
        return readFeature(entities, property_name)

    def setProperty(self, property_name, action, data):
        response = super().setProperty(property_name, action, data)
        self.clear_cache()
        return response

    def __get_or_update_cache(self):
        with self.__lock:
            if self.is_cache_invalid():
                self.__cache = self.fetch_all_features()
                self.__cacheTime = ViCareTimer().now()
            return self.__cache

    def is_cache_invalid(self) -> bool:
        return self.__cache is None or self.__cacheTime is None or (ViCareTimer().now() - self.__cacheTime).seconds > self.__cacheDuration

    def clear_cache(self):
        with self.__lock:
            self.__cache = None
            self.__cacheTime = None
