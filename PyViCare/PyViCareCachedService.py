from datetime import datetime
import threading
from PyViCare.PyViCareService import ViCareService, readFeature

# class is used to replace logic in unittest


class ViCareTimer:
    def now(self):
        return datetime.now()


class ViCareCachedService(ViCareService):

    def __init__(self, oauth_manager, accessor, cacheDuration):
        ViCareService.__init__(self, oauth_manager, accessor)
        self.cacheDuration = cacheDuration
        self.cache = None
        self.cacheTime = None
        self.lock = threading.Lock()

    def getProperty(self, property_name):
        data = self.__get_or_update_cache()
        entities = data["data"]
        return readFeature(entities, property_name)

    def setProperty(self, property_name, action, data):
        response = super().setProperty(property_name, action, data)
        self.clearCache()
        return response

    def __get_or_update_cache(self):
        with self.lock:
            if self.isCacheInvalid():
                url = f'/equipment/installations/{self.accessor.id}/gateways/{self.accessor.serial}/devices/{self.accessor.device_id}/features/'
                self.cache = self.oauth_manager.get(url)
                self.cacheTime = ViCareTimer().now()
            return self.cache

    def isCacheInvalid(self):
        return self.cache is None or self.cacheTime is None or (ViCareTimer().now() - self.cacheTime).seconds > self.cacheDuration

    def clearCache(self):
        with self.lock:
            self.cache = None
            self.cacheTime = None
