import logging
import threading
from typing import Any, List

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareService import (ViCareDeviceAccessor, ViCareService, ViCareServiceViaGateway, readFeature)
from PyViCare.PyViCareUtils import PyViCareInvalidDataError, PyViCareNotSupportedFeatureError, ViCareTimer

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

class ViCareCache:
    def __init__(self, cache_duration: int) -> None:
        self.cache_duration = cache_duration
        self.data = None
        self.cache_time = None
        self.lock = threading.Lock()

    def is_valid(self) -> bool:
        return self.data is not None and self.cache_time is not None and not (ViCareTimer().now() - self.cache_time).seconds > self.cache_duration

    def clear(self):
        with self.lock:
            self.data = None
            self.cache_time = None

    def set_cache(self, data: Any):
        with self.lock:
            self.data = data


class ViCareCachedServiceViaGateway(ViCareServiceViaGateway):
    def __init__(self, oauth_manager: AbstractViCareOAuthManager, accessor: ViCareDeviceAccessor, roles: List[str], cache: ViCareCache) -> None:
        ViCareServiceViaGateway.__init__(self, oauth_manager, accessor, roles)
        self.__cache = cache

    def getProperty(self, property_name: str) -> Any:
        data = self.__get_data()
        entities = data["data"]

    # def readFeature(entities, property_name):
        feature = next(
            (f for f in entities if f["feature"] == property_name), None)

        if feature is None:
            raise PyViCareNotSupportedFeatureError(property_name)

        return feature

        # return readFeature(entities, property_name)

    def setProperty(self, property_name, action, data):
        response = super().setProperty(property_name, action, data)
        self.__cache.clear()
        return response

    def fetch_all_features(self) -> Any:
        url = f'/features/installations/{self.accessor.id}/gateways/{self.accessor.serial}/features?includeDevicesFeatures=true'
        return self.oauth_manager.get(url)

    def __get_data(self):
        with self.__cache.lock:
            if not self.__cache.is_valid():
                # we always set the cache time before we fetch the data
                # to avoid consuming all the api calls if the api is down
                # see https://github.com/home-assistant/core/issues/67052
                # we simply return the old cache in this case
                self.__cache.cache_time = ViCareTimer().now()
                data = self.fetch_all_features()
                if "data" not in data:
                    logger.error("Missing 'data' property when fetching data.")
                    raise PyViCareInvalidDataError(data)
                self.__cache.set(data)
            return self.__cache.data
