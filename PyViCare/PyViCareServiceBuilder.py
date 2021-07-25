

from PyViCare.PyViCareOAuthManager import ViCareOAuthManager
from PyViCare.PyViCareCachedService import ViCareCachedService
from PyViCare.PyViCareService import ViCareService


class ViCareServiceBuilder:

    def __init__(self):
        self.circuitNumber = 0
        self.cacheDuration = 0

    def withCircuit(self, circuitNumber):
        self.circuitNumber = circuitNumber
        return self

    def withCacheDuration(self, cacheDurationInSeconds):
        self.cacheDuration = cacheDurationInSeconds
        return self

    def buildFromArgs(self, username, password, client_id, token_file=None):
        manager = ViCareOAuthManager(username, password, client_id, token_file)
        return self.buildFromOAuthManager(manager)

    def buildFromOAuthManager(self, oauth_manager):
        if self.cacheDuration == 0:
            return ViCareService(oauth_manager, self.circuitNumber)
        else:
            return ViCareCachedService(oauth_manager, self.circuitNumber)

