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

    # see: https://vitodata300.viessmann.com/vd300/ApplicationHelp/VD300/1031_de_DE/Ger%C3%A4teliste.html
    def asAutoDetectDevice(self):
        device_types = [
            (self.asGazBoiler, r"Vitodens|VScotH|Vitocrossal|VDensH|Vitopend|VPendH"),
            (self.asFuelCell, r"Vitovalor|Vitocharge|Vitoblo"),
            (self.asHeatPump, r"Vitocal|VBC70|V200WO1A|CU401B"),
            (self.asOilBoiler, r"Vitoladens|Vitoradial|Vitorondens|VPlusH"),
            (self.asPelletsBoiler, r"Vitoligno|Ecotronic|VBC550P")
        ]

        for (creator_method, type_name) in device_types:
            if re.search(type_name, self.device_model):
                logger.info("detected %s %s" %
                            (self.device_model, creator_method.__name__))
                return creator_method()

        logger.info(
            f"Could not auto detect {self.device_model}. Use generic device.")
        return self.asGeneric()

    def getRawJSON(self):
        return self.service.cache
