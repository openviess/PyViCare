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
        device_types = [
            (self.asGazBoiler, r"Vitodens"),
            (self.asFuelCell, r"Vitovalor|Vitocharge|Vitoblo"),
            (self.asHeatPump, r"Vitocal"),
            (self.asOilBoiler, r"Vitoladens|Vitoradial|Vitorondens"),
            (self.asPelletsBoiler, r"Vitoligno")
        ]

        for (creator_method, type_name) in device_types:
            if re.search(type_name, self.device_model):
                logger.info("detected %s %s" %
                            (self.device_model, creator_method.__name__))
                return creator_method()

        logger.info("Could not auto detect %s. Use generic device." %
                    self.device_model)
        return self.asGeneric()
