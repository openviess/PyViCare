import json
import logging
import re

from PyViCare.PyViCareFloorHeating import FloorHeating, FloorHeatingChannel
from PyViCare.PyViCareFuelCell import FuelCell
from PyViCare.PyViCareRoomControl import RoomControl
from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareHeatingDevice import HeatingDevice
from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareHybrid import Hybrid
from PyViCare.PyViCareOilBoiler import OilBoiler
from PyViCare.PyViCarePelletsBoiler import PelletsBoiler
from PyViCare.PyViCareRadiatorActuator import RadiatorActuator
from PyViCare.PyViCareRoomSensor import RoomSensor
from PyViCare.PyViCareRepeater import Repeater
from PyViCare.PyViCareElectricalEnergySystem import ElectricalEnergySystem
from PyViCare.PyViCareGateway import Gateway
from PyViCare.PyViCareService import (ViCareDeviceAccessor, ViCareService,
                                      hasRoles, is_gateway_role)
from PyViCare.PyViCareUtils import PyViCareNotPaidForError
from PyViCare.PyViCareVentilationDevice import VentilationDevice
from PyViCare.PyViCareWaterTreatment import WaterTreatment

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PyViCareDeviceConfig:
    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-instance-attributes
    def __init__(self, accessor: ViCareDeviceAccessor, service: ViCareService, device_model, status, device_type=None, roles=None):
        self.accessor = accessor
        self.service = service
        self.device_id = accessor.device_id
        self.device_model = device_model
        self.status = status
        self.device_type = device_type
        self.roles = roles if roles is not None else []

    def asGeneric(self):
        return HeatingDevice(self.accessor, self.service, self.roles)

    def asGazBoiler(self):
        return GazBoiler(self.accessor, self.service, self.roles)

    def asFuelCell(self):
        return FuelCell(self.accessor, self.service, self.roles)

    def asHeatPump(self):
        return HeatPump(self.accessor, self.service, self.roles)

    def asOilBoiler(self):
        return OilBoiler(self.accessor, self.service, self.roles)

    def asPelletsBoiler(self):
        return PelletsBoiler(self.accessor, self.service, self.roles)

    def asHybridDevice(self):
        return Hybrid(self.accessor, self.service, self.roles)

    def asRadiatorActuator(self):
        return RadiatorActuator(self.accessor, self.service, self.roles)

    def asFloorHeating(self):
        return FloorHeating(self.accessor, self.service, self.roles)

    def asFloorHeatingChannel(self):
        return FloorHeatingChannel(self.accessor, self.service, self.roles)

    def asRoomSensor(self):
        return RoomSensor(self.accessor, self.service, self.roles)

    def asRoomControl(self):
        return RoomControl(self.accessor, self.service, self.roles)

    def asRepeater(self):
        return Repeater(self.accessor, self.service, self.roles)

    def asElectricalEnergySystem(self):
        return ElectricalEnergySystem(self.accessor, self.service, self.roles)

    def asGateway(self):
        return Gateway(self.accessor, self.service, self.roles)

    def asVentilation(self):
        return VentilationDevice(self.accessor, self.service, self.roles)

    def asWaterTreatment(self):
        return WaterTreatment(self.service)

    def getConfig(self):
        return self.accessor

    def getId(self):
        return self.device_id

    def getModel(self):
        return self.device_model

    def isOnline(self):
        return self.status == "Online"

    def getDeviceType(self):
        return self.device_type

    def getRoles(self):
        return self.roles

    def hasRoles(self, requested_roles):
        return hasRoles(requested_roles, self.roles)

    def isGateway(self):
        return is_gateway_role(self.roles)

    # see: https://vitodata300.viessmann.com/vd300/ApplicationHelp/VD300/1031_de_DE/Ger%C3%A4teliste.html
    def asAutoDetectDevice(self):
        device_types = [
            (self.asFuelCell, r"Vitovalor|Vitocharge|Vitoblo", []),
            (self.asPelletsBoiler, r"Vitoligno|Ecotronic|VBC550P", []),
            (self.asOilBoiler, r"Vitoladens|Vitoradial|Vitorondens|VPlusH|V200KW2_6", []),
            (self.asGazBoiler, r"Vitodens|VScotH|Vitocrossal|VDensH|Vitopend|VPendH|OT_Heating_System", ["type:boiler"]),
            (self.asHeatPump, r"Vitocal|VBC70|V200WO1A|CU401B", ["type:heatpump"]),
            (self.asElectricalEnergySystem, r"E3_VitoCharge_03", ["type:ees"]), # ees, it this a typo?
            (self.asElectricalEnergySystem, r"E3_VitoCharge_05", ["type:ess"]),
            (self.asVentilation, r"E3_ViAir", ["type:ventilation"]),
            (self.asVentilation, r"E3_ViAir", ["type:ventilation;central"]),
            (self.asVentilation, r"E3_VitoPure", ["type:ventilation;purifier"]),
            (self.asRadiatorActuator, r"E3_RadiatorActuator", ["type:radiator"]),
            (self.asFloorHeating, r"Smart_zigbee_fht_main|E3_FloorHeatingCircuitDistributorBox", ["type:fhtMain"]),
            (self.asFloorHeatingChannel, r"Smart_zigbee_fht_channel", ["type:fhtChannel"]),
            (self.asRoomControl, r"E3_RoomControl|Smart_RoomControl", ["type:virtual;smartRoomControl"]),
            (self.asRoomSensor, r"E3_RoomSensor", ["type:climateSensor"]),
            (self.asRepeater, r"E3_Repeater", ["type:repeater"]),
            (self.asWaterTreatment, r"VitosetAqua", ["type:waterTreatment"]),
            (self.asGateway, r"E3_TCU41_x04", ["type:gateway;TCU100"]),
            (self.asGateway, r"E3_TCU19_x05", ["type:gateway;TCU200"]),
            (self.asGateway, r"E3_TCU10_x07", ["type:gateway;TCU300"]),
            (self.asGateway, r"Heatbox1", ["type:gateway;VitoconnectOpto1"]),
            (self.asGateway, r"Heatbox2", ["type:gateway;VitoconnectOpto2/OT2"])
        ]

        for (creator_method, type_name, roles) in device_types:
            if re.search(type_name, self.device_model) or self.hasRoles(roles):
                logger.info("detected %s %s", self.device_model, creator_method.__name__)
                device = creator_method()
                if isinstance(device, (GazBoiler, HeatPump)) and not isinstance(device, Hybrid):
                    if self._isHybridByFeatures():
                        logger.info("upgrading %s to Hybrid based on API features", self.device_model)
                        return self.asHybridDevice()
                return device

        logger.info("Could not auto detect %s. Use generic device.", self.device_model)
        return self.asGeneric()

    def _isHybridByFeatures(self):
        """Check API features to detect hybrid devices (both burners and compressors)."""
        try:
            features = self.service.fetch_all_features(self.accessor)
            feature_names = [f["feature"] for f in features.get("data", [])]
            has_burners = any(f.startswith("heating.burners") for f in feature_names)
            has_compressors = any(f.startswith("heating.compressors") for f in feature_names)
            return has_burners and has_compressors
        except PyViCareNotPaidForError:
            # Account lacks the paid feature package, so feature listing is
            # unavailable. Treat as non-hybrid and let downstream feature
            # access fall back to PyViCareNotSupportedFeatureError via the
            # cached service. Without this, auto-detection crashes the
            # integration setup before any device is created.
            logger.debug("PACKAGE_NOT_PAID_FOR while detecting hybrid for %s, treating as non-hybrid", self.device_model)
            return False
        except (KeyError, TypeError, AttributeError, OSError):
            logger.debug("Could not fetch features for hybrid detection of %s", self.device_model)
            return False

    def get_raw_json(self):
        return self.service.fetch_all_features(self.accessor)

    def dump_secure(self, flat=False):
        device_info = {
            "id": self.device_id,
            "modelId": self.device_model,
            "type": self.device_type,
            "status": self.status,
            "roles": self.roles
        }
        try:
            raw_data = self.get_raw_json()
            data = raw_data['data']
        except PyViCareNotPaidForError:
            # Feature listing requires a paid package the account does not
            # have. Emit a placeholder so diagnostics still produce a usable
            # dump (device metadata plus an unavailable-reason marker)
            # rather than crashing the diagnostics endpoint.
            logger.debug("PACKAGE_NOT_PAID_FOR while dumping features for %s", self.device_model)
            data = []
            device_info["dataUnavailableReason"] = "PACKAGE_NOT_PAID_FOR"
        output = {
            "device": device_info,
            "data": data
        }

        if flat:
            inner = ',\n'.join([json.dumps(x, sort_keys=True) for x in output['data']])
            outer = json.dumps({'device': output['device'], 'data': ['placeholder']}, indent=0, sort_keys=True)
            dumpJSON = outer.replace('"placeholder"', inner)
        else:
            dumpJSON = json.dumps(output, indent=4, sort_keys=True)

        def repl(m):
            return m.group(1) + ('#' * len(m.group(2))) + m.group(3)

        return re.sub(r'(["\/])(\d{6,})(["\/])', repl, dumpJSON)
