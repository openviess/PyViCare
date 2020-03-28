from datetime import datetime

from PyViCare.PyViCareService import apiURLBase, ViCareService

class ViCareCachedService(ViCareService):
    
    def __init__(self, username, password, cacheDuration, token_file=None,circuit=0):
        ViCareService.__init__(self, username, password, token_file, circuit)
        self.cacheDuration = cacheDuration
        self.cache = None
        self.cacheTime = None

    def __setCache(self):
        url = apiURLBase + '/operational-data/installations/' + str(self.id) + '/gateways/' + str(self.serial) + '/devices/0/features/'
        self.cache = self.get(url)
        self.cacheTime = datetime.now()

    def getProperty(self,property_name):
        if self.cache is None or self.cacheTime is None or (datetime.now() - self.cacheTime).seconds > self.cacheDuration:
            self.__setCache()
        
        entities = self.cache["entities"]
        feature = next((f for f in entities if f["class"][0] == property_name and f["class"][1] == "feature"), {})
        return feature