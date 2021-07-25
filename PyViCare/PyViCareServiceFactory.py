

from PyViCare.PyViCareOAuthManager import ViCareOAuthManager
from PyViCare.PyViCareCachedService import ViCareCachedService
from PyViCare.PyViCareService import ViCareService


class ViCareServiceFactory:

    @staticmethod
    def buildFromArgs(username, password, client_id, token_file=None, circuit=0,cacheDuration=0):
        manager = ViCareOAuthManager(username, password, client_id, token_file)
        return ViCareServiceFactory.buildFromOAuthManager(manager, circuit, cacheDuration)

    @staticmethod
    def buildFromOAuthManager(oauth_manager, circuit=0, cacheDuration=0):
        if cacheDuration == 0:
            return ViCareService(oauth_manager, circuit)
        else:
            return ViCareCachedService(oauth_manager, circuit)

