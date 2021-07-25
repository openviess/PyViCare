from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareOAuthManager import ViCareOAuthManager
from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareFuelCell import FuelCell
from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareOilBoiler import OilBoiler
from PyViCare.PyViCarePelletsBoiler import PelletsBoiler
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareCachedService import ViCareCachedService
from PyViCare.PyViCareService import ViCareService


class PyViCareDeviceConfig:
    def __init__(self, service):
        self.service = service

    def asGeneric(self):
        return Device(self.service)

    def asGazBoiler(self):
        return GazBoiler(self.service)

    def asFuelCell(self):
        return FuelCell(self.service)

    def asHeatPump(self):
        return HeatPump(self.service)

    def asOilBoiler(self):
        return OilBoiler(self.service)

    def asPelletsBoilder(self):
        return PelletsBoiler(self.service)

class PyViCare:
    def __init__(self):
        self.cacheDuration = 60

    def setCacheDuration(self, cache_duration):
        self.cacheDuration = cache_duration

    def init(self, username, password, client_id, token_file):
        self.oauth_manager = ViCareOAuthManager(username, password, client_id, token_file)
        self.__loadInstallations()

    def init(self, oauth_manager):
        self.oauth_manager = oauth_manager
        self.__loadInstallations()

    def __buildService(self, accessor):
        if self.cacheDuration > 0:
            return ViCareCachedService(self.oauth_manager, accessor, self.cacheDuration)
        else:
            return ViCareService(self.oauth_manager, accessor)

    def __loadInstallations(self):
        installations = self.oauth_manager.get("/equipment/installations?includeGateways=true")
        installation = installations["data"][0]
        id = installation["id"]
        serial = installation["gateways"][0]["serial"]
        self.devices[0] = ViCareDeviceAccessor(id, serial, 0)

    def device(self, index):
        return PyViCareDeviceConfig(self.__buildService(self.devices[index]))


    