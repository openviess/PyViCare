import json
import logging
import re

from PyViCare.generic.PyViCareGenericDevice import GenericDevice
from PyViCare.heating.PyViCareFuelCell import FuelCell
from PyViCare.heating.PyViCareGazBoiler import GazBoiler
from PyViCare.heating.PyViCareHeatPump import HeatPump
from PyViCare.heating.PyViCareHybrid import Hybrid
from PyViCare.heating.PyViCareOilBoiler import OilBoiler
from PyViCare.heating.PyViCarePelletsBoiler import PelletsBoiler
from PyViCare.radiator.PyViCareRadiatorActuator import RadiatorActuator
from PyViCare.sensor.PyViCareRoomSensor import RoomSensor

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())


class PyViCareDeviceConfig:
    def __init__(self, service, device_id, device_model, status):
        self.service = service
        self.device_id = device_id
        self.device_model = device_model
        self.status = status

    def asGeneric(self):
        return GenericDevice(self.service)

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

    def asHybridDevice(self):
        return Hybrid(self.service)

    def asRadiatorActuator(self):
        return RadiatorActuator(self.service)

    def asRoomSensor(self):
        return RoomSensor(self.service)

    def getConfig(self):
        return self.service.accessor

    def getId(self):
        return self.device_id

    def getModel(self):
        return self.device_model

    def isOnline(self):
        return self.status == "Online"

    # see: https://vitodata300.viessmann.com/vd300/ApplicationHelp/VD300/1031_de_DE/Ger%C3%A4teliste.html
    def asAutoDetectDevice(self):
        device_types = [
            (self.asFuelCell, r"Vitovalor|Vitocharge|Vitoblo", []),
            (self.asGazBoiler, r"Vitodens|VScotH|Vitocrossal|VDensH|Vitopend|VPendH|OT_Heating_System", ["type:boiler"]),
            (self.asHeatPump, r"Vitocal|VBC70|V200WO1A|CU401B", ["type:heatpump"]),
            (self.asOilBoiler, r"Vitoladens|Vitoradial|Vitorondens|VPlusH|V200KW2_6", []),
            (self.asPelletsBoiler, r"Vitoligno|Ecotronic|VBC550P", []),
            (self.asRadiatorActuator, r"E3_RadiatorActuator", ["type:radiator"]),
            (self.asRoomSensor, r"E3_RoomSensor", ["type:climateSensor"])
        ]

        for (creator_method, type_name, roles) in device_types:
            if re.search(type_name, self.device_model) or self.service.hasRoles(roles):
                logger.info("detected %s %s" %
                            (self.device_model, creator_method.__name__))
                return creator_method()

        logger.info(
            f"Could not auto detect {self.device_model}. Use generic device.")
        return self.asGeneric()

    def get_raw_json(self):
        return self.service.fetch_all_features()

    def dump_secure(self, flat=False):
        if flat:
            inner = ',\n'.join([json.dumps(x, sort_keys=True) for x in self.get_raw_json()['data']])
            outer = json.dumps({'data': ['placeholder']}, indent=0)
            dumpJSON = outer.replace('"placeholder"', inner)
        else:
            dumpJSON = json.dumps(self.get_raw_json(), indent=4, sort_keys=True)

        def repl(m):
            return m.group(1) + ('#' * len(m.group(2))) + m.group(3)

        return re.sub(r'(["\/])(\d{6,})(["\/])', repl, dumpJSON)
