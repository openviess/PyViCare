from PyViCare.PyViCareServiceBuilder import ViCareServiceBuilder
from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareFuelCell import FuelCell
from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareOilBoiler import OilBoiler
from PyViCare.PyViCarePelletsBoiler import PelletsBoiler

class PyViCare:
    def __init__(self):
        return

    def init(self, username, password, client_id, token_file):
        self.service = ViCareServiceBuilder.buildFromArgs(username, password, client_id, token_file)

    def init(self, oauth_manager):
        self.service = ViCareServiceBuilder.buildFromOAuthManager(oauth_manager)

    def getGazBoilerDevice(self):
        return GazBoiler(self.service)

    def getFuelCellDevice(self):
        return FuelCell(self.service)

    def getHeatPumpDevice(self):
        return HeatPump(self.service)

    def getOilBoilerDevice(self):
        return OilBoiler(self.service)

    def getPelletsBoilderDevice(self):
        return PelletsBoiler(self.service)


    