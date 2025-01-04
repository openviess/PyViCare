import json
import logging
import re

from PyViCare.PyViCareFuelCell import FuelCell
from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareHeatingDevice import HeatingDevice
from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareHybrid import Hybrid
from PyViCare.PyViCareOilBoiler import OilBoiler
from PyViCare.PyViCarePelletsBoiler import PelletsBoiler
from PyViCare.PyViCareRadiatorActuator import RadiatorActuator
from PyViCare.PyViCareRoomSensor import RoomSensor
from PyViCare.PyViCareElectricalEnergySystem import ElectricalEnergySystem
from PyViCare.PyViCareGateway import Gateway
from PyViCare.PyViCareVentilationDevice import VentilationDevice

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())


class PyViCareDeviceConfig:
    def __init__(self, service, device_id, device_model, status):
        self.service = service
        self.device_id = device_id
        self.device_model = device_model
        self.status = status

    def asGeneric(self):
        return HeatingDevice(self.service)

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

    def asElectricalEnergySystem(self):
        return ElectricalEnergySystem(self.service)

    def asGateway(self):
        return Gateway(self.service)

    def asVentilation(self):
        return VentilationDevice(self.service)

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
            (self.asElectricalEnergySystem, r"E3_VitoCharge_03", ["type:ees"]), # ees, it this a typo?
            (self.asElectricalEnergySystem, r"E3_VitoCharge_05", ["type:ess"]),
            (self.asVentilation, r"E3_ViAir", ["type:ventilation"]),
            (self.asVentilation, r"E3_ViAir", ["type:ventilation;central"]),
            (self.asVentilation, r"E3_VitoPure", ["type:ventilation;purifier"]),
            (self.asRadiatorActuator, r"E3_RadiatorActuator", ["type:radiator"]),
            (self.asRoomSensor, r"E3_RoomSensor", ["type:climateSensor"]),
            (self.asGateway, r"E3_TCU41_x04", ["type:gateway;TCU100"]),
            (self.asGateway, r"E3_TCU19_x05", ["type:gateway;TCU200"]),
            (self.asGateway, r"E3_TCU10_x07", ["type:gateway;TCU300"]),
            (self.asGateway, r"Heatbox1", ["type:gateway;VitoconnectOpto1"]),
            (self.asGateway, r"Heatbox2", ["type:gateway;VitoconnectOpto2/OT2"])
        ]

        for (creator_method, type_name, roles) in device_types:
            if re.search(type_name, self.device_model) or self.service.hasRoles(roles):
                logger.info("detected %s %s", self.device_model, creator_method.__name__)
                return creator_method()

        logger.info("Could not auto detect %s. Use generic device.", self.device_model)
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
