import json
import unittest
from unittest.mock import Mock

from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareService import ViCareDeviceAccessor, hasRoles
from PyViCare.PyViCareUtils import PyViCareNotPaidForError


def has_roles(roles):
    return lambda requested_roles: hasRoles(requested_roles, roles)


class PyViCareDeviceConfigTest(unittest.TestCase):

    def setUp(self) -> None:
        self.service = Mock()
        self.service.hasRoles = has_roles([])
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")

    def test_autoDetect_Vitodens_asGazBoiler(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "E3_Vitodens_200_xxxx/E3_Dictionary", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_Unknown_asGeneric(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "myRobot", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatingDevice", type(device_type).__name__)

    def test_autoDetect_VScot_asGazBoiler(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "VScotHO1_200", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_RoleBoiler_asGazBoiler(self):
        self.service.hasRoles = has_roles(["type:boiler"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_RoleHeatpump_asHeatpump(self):
        self.service.hasRoles = has_roles(["type:heatpump"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatPump", type(device_type).__name__)

    def test_autoDetect_RoleRadiator_asRadiatorActuator(self):
        self.service.hasRoles = has_roles(["type:radiator"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("RadiatorActuator", type(device_type).__name__)

    def test_autoDetect_RoleClimateSensor_asRoomSensor(self):
        self.service.hasRoles = has_roles(["type:climateSensor"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("RoomSensor", type(device_type).__name__)

    def test_autoDetect_RoleVentilation_asVentilation(self):
        self.service.hasRoles = has_roles(["type:ventilation"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_RoleVentilationCentral_asVentilation(self):
        self.service.hasRoles = has_roles(["type:ventilation;central"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_Vitoair_FS_300F_asVentilation(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "E3_ViAir_300F", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_RoleVentilationPurifier_asVentilation(self):
        self.service.hasRoles = has_roles(["type:ventilation;purifier"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_Vitopure_350_asVentilation(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "E3_VitoPure", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_RoleESS_asElectricalEnergySystem(self):
        self.service.hasRoles = has_roles(["type:ess"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("ElectricalEnergySystem", type(device_type).__name__)

    def test_autoDetect_E3_RoomControl_asRoomControl(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "E3_RoomControl_One_525", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("RoomControl", type(device_type).__name__)

    def test_autoDetect_Smart_RoomControl_asRoomControl(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Smart_RoomControl", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("RoomControl", type(device_type).__name__)

    def test_autoDetect_RoleRoomControl_asRoomControl(self):
        self.service.hasRoles = has_roles(["type:virtual;smartRoomControl"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("RoomControl", type(device_type).__name__)

    def test_autoDetect_Vitocharge05_asElectricalEnergySystem(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "E3_VitoCharge_05", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("ElectricalEnergySystem", type(device_type).__name__)

    def test_autoDetect_VitoconnectOpto1_asGateway(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Heatbox1", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_VitoconnectOpto2_asGateway(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Heatbox2_SRC", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_TCU100_asGateway(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "E3_TCU41_x04", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_TCU200_asGateway(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "E3_TCU19_x05", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_TCU300_asGateway(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "E3_TCU10_x07", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_Ecotronic_asPelletsBoiler(self):
        self.service.hasRoles = has_roles(["type:boiler"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Ecotronic", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("PelletsBoiler", type(device_type).__name__)

    def test_autoDetect_Vitoladens_asOilBoiler(self):
        self.service.hasRoles = has_roles(["type:boiler"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitoladens", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("OilBoiler", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway(self):
        self.service.hasRoles = has_roles(["type:gateway;VitoconnectOpto1"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_vc_opto2(self):
        self.service.hasRoles = has_roles(["type:gateway;VitoconnectOpto2/OT2"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_TCU100(self):
        self.service.hasRoles = has_roles(["type:gateway;TCU100"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_TCU200(self):
        self.service.hasRoles = has_roles(["type:gateway;TCU200"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_TCU300(self):
        self.service.hasRoles = has_roles(["type:gateway;TCU300"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_legacy_device(self):
        self.service.hasRoles = has_roles(["type:legacy"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device = c.asAutoDetectDevice()
        self.assertEqual(device.isLegacyDevice(), True)
        self.assertEqual(device.isE3Device(), False)

    def test_e3_device(self):
        self.service.hasRoles = has_roles(["type:E3"])
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online")
        device = c.asAutoDetectDevice()
        self.assertEqual(device.isLegacyDevice(), False)
        self.assertEqual(device.isE3Device(), True)

    def test_autoDetect_CU401B_S_with_burners_and_compressors_asHybrid(self):
        self.service.hasRoles = has_roles(["type:heatpump"])
        self.service.fetch_all_features = Mock(return_value={"data": [
            {"feature": "heating.burners"},
            {"feature": "heating.burners.0"},
            {"feature": "heating.compressors"},
            {"feature": "heating.compressors.0"},
        ]})
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "CU401B_S", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Hybrid", type(device_type).__name__)

    def test_autoDetect_HeatPump_without_burners_stays_HeatPump(self):
        self.service.hasRoles = has_roles(["type:heatpump"])
        self.service.fetch_all_features = Mock(return_value={"data": [
            {"feature": "heating.compressors"},
            {"feature": "heating.compressors.0"},
        ]})
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitocal300", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatPump", type(device_type).__name__)

    def test_autoDetect_GazBoiler_with_compressors_asHybrid(self):
        self.service.hasRoles = has_roles(["type:boiler"])
        self.service.fetch_all_features = Mock(return_value={"data": [
            {"feature": "heating.burners"},
            {"feature": "heating.burners.0"},
            {"feature": "heating.compressors"},
            {"feature": "heating.compressors.0"},
        ]})
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitodens200", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Hybrid", type(device_type).__name__)

    def test_autoDetect_feature_fetch_failure_keeps_original(self):
        self.service.hasRoles = has_roles(["type:heatpump"])
        self.service.fetch_all_features = Mock(side_effect=OSError("API error"))
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "CU401B_S", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatPump", type(device_type).__name__)

    def test_autoDetect_NotPaidFor_keeps_original(self):
        self.service.hasRoles = has_roles(["type:heatpump"])
        self.service.fetch_all_features = Mock(
            side_effect=PyViCareNotPaidForError({"errorType": "PACKAGE_NOT_PAID_FOR"}))
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "CU401B_S", "Online")
        device_type = c.asAutoDetectDevice()
        # Without the fix, asAutoDetectDevice would propagate the exception
        # and crash integration setup. With the fix, hybrid detection falls
        # back to non-hybrid and the device is created as HeatPump.
        self.assertEqual("HeatPump", type(device_type).__name__)

    def test_dump_secure_NotPaidFor_emits_placeholder(self):
        self.service.fetch_all_features = Mock(
            side_effect=PyViCareNotPaidForError({"errorType": "PACKAGE_NOT_PAID_FOR"}))
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "CU401B_S", "Online")
        dump = json.loads(c.dump_secure())
        # Diagnostics should produce a usable dump rather than crashing
        # when the account lacks the paid feature package.
        self.assertEqual(dump["device"]["dataUnavailableReason"], "PACKAGE_NOT_PAID_FOR")
        self.assertEqual(dump["data"], [])

    def test_getDeviceType_heating(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitocal", "Online", "heating")
        self.assertEqual(c.getDeviceType(), "heating")

    def test_getDeviceType_vitoconnect(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Heatbox1", "Online", "vitoconnect")
        self.assertEqual(c.getDeviceType(), "vitoconnect")


    def test_getDeviceType_none_when_not_provided(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitocal", "Online")
        self.assertIsNone(c.getDeviceType())

    def test_getRoles(self):
        roles = ["type:heatpump", "type:E3"]
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitocal", "Online", "heating", roles)
        self.assertEqual(c.getRoles(), roles)

    def test_getRoles_empty_when_not_provided(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitocal", "Online")
        self.assertEqual(c.getRoles(), [])

    def test_isGateway_true_for_gateway_role(self):
        self.service._isGateway = Mock(return_value=True)  # pylint: disable=protected-access
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Heatbox1", "Online", "vitoconnect")
        self.assertTrue(c.isGateway())

    def test_isGateway_false_for_non_gateway_role(self):
        self.service._isGateway = Mock(return_value=False)  # pylint: disable=protected-access
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitocal", "Online", "heating")
        self.assertFalse(c.isGateway())
