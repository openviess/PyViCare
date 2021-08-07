from datetime import datetime
import threading
from PyViCare.PyViCareService import ViCareService, readFeature


class ViCareTimer:
    # class is used to replace logic in unittest
    def now(self):
        return datetime.now()


class ViCareCachedService(ViCareService):

    def __init__(self, oauth_manager, accessor, cacheDuration):
        ViCareService.__init__(self, oauth_manager, accessor)
        self.__cacheDuration = cacheDuration
        self.__cache = None
        self.__cacheTime = None
        self.__lock = threading.Lock()

    def getProperty(self, property_name):
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
                url = f'/equipment/installations/{self.accessor.id}/gateways/{self.accessor.serial}/devices/{self.accessor.device_id}/features/'
                self.__cache = self.oauth_manager.get(url)
                self.__cacheTime = ViCareTimer().now()
            return self.__cache

    def is_cache_invalid(self):
        return self.__cache is None or self.__cacheTime is None or (ViCareTimer().now() - self.__cacheTime).seconds > self.__cacheDuration

    def clear_cache(self):
        with self.__lock:
            self.__cache = None
            self.__cacheTime = None
