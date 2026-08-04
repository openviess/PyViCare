import json
import unittest
from unittest.mock import Mock

from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import PyViCareNotPaidForError


class PyViCareDeviceConfigTest(unittest.TestCase):

    def setUp(self) -> None:
        self.service = Mock()
        self.accessor = ViCareDeviceAccessor(0, "[serial]", "0")

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
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:boiler"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_RoleHeatpump_asHeatpump(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:heatpump"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatPump", type(device_type).__name__)

    def test_autoDetect_RoleRadiator_asRadiatorActuator(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:radiator"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("RadiatorActuator", type(device_type).__name__)

    def test_autoDetect_RoleClimateSensor_asRoomSensor(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:climateSensor"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("RoomSensor", type(device_type).__name__)

    def test_autoDetect_RoleVentilation_asVentilation(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:ventilation"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_RoleVentilationCentral_asVentilation(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:ventilation;central"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_Vitoair_FS_300F_asVentilation(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "E3_ViAir_300F", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_RoleVentilationPurifier_asVentilation(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:ventilation;purifier"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_Vitopure_350_asVentilation(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "E3_VitoPure", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_RoleESS_asElectricalEnergySystem(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:ess"])
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
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:virtual;smartRoomControl"])
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
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Ecotronic", "Online", roles=["type:boiler"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("PelletsBoiler", type(device_type).__name__)

    def test_autoDetect_Vitoladens_asOilBoiler(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitoladens", "Online", roles=["type:boiler"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("OilBoiler", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:gateway;VitoconnectOpto1"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_vc_opto2(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:gateway;VitoconnectOpto2/OT2"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_TCU100(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:gateway;TCU100"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_TCU200(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:gateway;TCU200"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_TCU300(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:gateway;TCU300"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_VitosetAqua19D_asWaterTreatment(self):
        c = PyViCareDeviceConfig(self.service, "0", "VitosetAqua19D", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("WaterTreatment", type(device_type).__name__)

    def test_autoDetect_VitosetAqua42D_asWaterTreatment(self):
        c = PyViCareDeviceConfig(self.service, "0", "VitosetAqua42D", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("WaterTreatment", type(device_type).__name__)

    def test_autoDetect_RoleWaterTreatment_asWaterTreatment(self):
        self.service.hasRoles = has_roles(["type:waterTreatment"])
        c = PyViCareDeviceConfig(self.service, "0", "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("WaterTreatment", type(device_type).__name__)

    def test_legacy_device(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:legacy"])
        device = c.asAutoDetectDevice()
        self.assertEqual(device.isLegacyDevice(), True)
        self.assertEqual(device.isE3Device(), False)

    def test_e3_device(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Unknown", "Online", roles=["type:E3"])
        device = c.asAutoDetectDevice()
        self.assertEqual(device.isLegacyDevice(), False)
        self.assertEqual(device.isE3Device(), True)

    def test_autoDetect_CU401B_S_with_burners_and_compressors_asHybrid(self):
        self.service.fetch_all_features = Mock(return_value={"data": [
            {"feature": "heating.burners"},
            {"feature": "heating.burners.0"},
            {"feature": "heating.compressors"},
            {"feature": "heating.compressors.0"},
        ]})
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "CU401B_S", "Online", roles=["type:heatpump"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Hybrid", type(device_type).__name__)

    def test_autoDetect_HeatPump_without_burners_stays_HeatPump(self):
        self.service.fetch_all_features = Mock(return_value={"data": [
            {"feature": "heating.compressors"},
            {"feature": "heating.compressors.0"},
        ]})
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitocal300", "Online", roles=["type:heatpump"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatPump", type(device_type).__name__)

    def test_autoDetect_GazBoiler_with_compressors_asHybrid(self):
        self.service.fetch_all_features = Mock(return_value={"data": [
            {"feature": "heating.burners"},
            {"feature": "heating.burners.0"},
            {"feature": "heating.compressors"},
            {"feature": "heating.compressors.0"},
        ]})
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitodens200", "Online", roles=["type:boiler"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Hybrid", type(device_type).__name__)

    def test_autoDetect_feature_fetch_failure_keeps_original(self):
        self.service.fetch_all_features = Mock(side_effect=OSError("API error"))
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "CU401B_S", "Online", roles=["type:heatpump"])
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatPump", type(device_type).__name__)

    def test_autoDetect_NotPaidFor_keeps_original(self):
        self.service.fetch_all_features = Mock(
            side_effect=PyViCareNotPaidForError({"errorType": "PACKAGE_NOT_PAID_FOR"}))
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "CU401B_S", "Online", roles=["type:heatpump"])
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
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Heatbox1", "Online", "vitoconnect",
            roles=["type:gateway;VitoconnectOpto1"])
        self.assertTrue(c.isGateway())

    def test_isGateway_false_for_non_gateway_role(self):
        c = PyViCareDeviceConfig(
            self.accessor, self.service, "Vitocal", "Online", "heating",
            roles=["type:heatpump"])
        self.assertFalse(c.isGateway())
