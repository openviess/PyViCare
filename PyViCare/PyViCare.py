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
    def __init__(self, service, device_model, status):
        self.service = service
        self.device_model = device_model
        self.status = status

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

    def getConfig(self):
        return self.service.accessor

    def getModel(self):
        return self.device_model

    def isOnline(self):
        return self.status == "Online"


class ViCare:
    def __init__(self):
        self.cacheDuration = 60

    def setCacheDuration(self, cache_duration):
        self.cacheDuration = cache_duration

    def initWithCredentials(self, username, password, client_id, token_file):
        self.oauth_manager = ViCareOAuthManager(
            username, password, client_id, token_file)
        self.__loadInstallations()

    def initWithExternalOAuth(self, oauth_manager):
        self.oauth_manager = oauth_manager
        self.__loadInstallations()

    def __buildService(self, accessor):
        if self.cacheDuration > 0:
            return ViCareCachedService(self.oauth_manager, accessor, self.cacheDuration)
        else:
            return ViCareService(self.oauth_manager, accessor)

    def __loadInstallations(self):
        installations = self.oauth_manager.get(
            "/equipment/installations?includeGateways=true")
        self.devices = []
        for installation in installations["data"]:
            installation_id = installation["id"]

            for gateway in installation["gateways"]:
                gateway_serial = gateway["serial"]

                for device in gateway["devices"]:
                    if device["deviceType"] != "heating":
                        continue  # we are not interested in non heating devices

                    device_id = device["id"]
                    device_model = device["modelId"]
                    status = device["status"]

                    accessor = ViCareDeviceAccessor(
                        installation_id, gateway_serial, device_id)
                    service = self.__buildService(accessor)

                    self.devices.append(PyViCareDeviceConfig(
                        service, device_model, status))
