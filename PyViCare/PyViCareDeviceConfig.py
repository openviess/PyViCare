from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareFuelCell import FuelCell
from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareOilBoiler import OilBoiler
from PyViCare.PyViCarePelletsBoiler import PelletsBoiler
import re
import logging
logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())


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

    def asPelletsBoiler(self):
        return PelletsBoiler(self.service)

    def getConfig(self):
        return self.service.accessor

    def getModel(self):
        return self.device_model

    def isOnline(self):
        return self.status == "Online"

    def asAutoDetectDevice(self):
        if re.search(r"Vitodens", self.device_model):
            logger.info("detected %s as GazBoiler" % self.device_model)
            return self.asGazBoiler()
        if re.search(r"Vitovalor|Vitocharge|Vitobloc", self.device_model):
            logger.info("detected %s as FuelCell" % self.device_model)
            return self.asFuelCell()
        if re.search(r"Vitocal", self.device_model):
            logger.info("detected %s as HeatPump" % self.device_model)
            return self.asHeatPump()
        if re.search(r"Vitoladens|Vitoradial|Vitorondens", self.device_model):
            logger.info("detected %s as OilBoiler" % self.device_model)
            return self.asOilBoiler()
        if re.search(r"Vitoligno", self.device_model):
            logger.info("detected %s as PelletsBoiler" % self.device_model)
            return self.asPelletsBoiler()

        print("Could not auto detect %s. Use generic device." % self.device_model)
        return self.asGeneric()



