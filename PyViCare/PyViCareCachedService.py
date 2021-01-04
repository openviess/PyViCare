from datetime import datetime
import threading
from PyViCare.PyViCareService import apiURLBase, ViCareService, readFeature

class ViCareCachedService(ViCareService):
    
    def __init__(self, username, password, cacheDuration, token_file=None,circuit=0):
        ViCareService.__init__(self, username, password, token_file, circuit)
        self.cacheDuration = cacheDuration
        self.cache = None
        self.cacheTime = None
        self.lock = threading.Lock()


    def getProperty(self,property_name):
        data = self.getOrUpdateCache()   
        entities = data["entities"]
        return readFeature(entities, property_name)

    def setProperty(self,property_name,action,data):
        response = super().setProperty(property_name, action, data)
        self.clearCache()
        return response

    def getOrUpdateCache(self):
        self.lock.acquire()
        try:
            if self.isCacheInvalid():
                url = apiURLBase + '/operational-data/installations/' + str(self.id) + '/gateways/' + str(self.serial) + '/devices/0/features/'
                self.cache = self.get(url)
                self.cacheTime = datetime.now()
            return self.cache
        finally:
            self.lock.release()

    def isCacheInvalid(self):
        return self.cache is None or self.cacheTime is None or (datetime.now() - self.cacheTime).seconds > self.cacheDuration

    def clearCache(self):
        self.lock.acquire()
        try:
            self.cache = None
            self.cacheTime = None
        finally:
            self.lock.release()
