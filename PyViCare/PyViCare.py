from PyViCare.PyViCareServiceBuilder import ViCareServiceBuilder
from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareFuelCell import FuelCell
from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareOilBoiler import OilBoiler
from PyViCare.PyViCarePelletsBoiler import PelletsBoiler
from PyViCare.PyViCareService import ViCareDeviceAccessor


class PyViCare:
    def __init__(self):
        return

    def init(self, username, password, client_id, token_file):
        self.service = ViCareServiceBuilder.buildFromArgs(username, password, client_id, token_file)
        self.__loadInstallations()

    def init(self, oauth_manager):
        self.service = ViCareServiceBuilder.buildFromOAuthManager(oauth_manager)
        self.__loadInstallations()

    def __loadInstallations(self):
        installations = self.service.get("/equipment/installations?includeGateways=true")
        installation = installations["data"][0]
        id = installation["id"]
        serial = installation["gateways"][0]["serial"]
        self.accessor = ViCareDeviceAccessor(self.service, id, serial, 0)

    def getGazBoilerDevice(self):
        return GazBoiler(self.accessor)

    def getFuelCellDevice(self):
        return FuelCell(self.accessor)

    def getHeatPumpDevice(self):
        return HeatPump(self.accessor)

    def getOilBoilerDevice(self):
        return OilBoiler(self.accessor)

    def getPelletsBoilderDevice(self):
        return PelletsBoiler(self.accessor)


    