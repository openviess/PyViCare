import unittest
from unittest.mock import Mock

from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareService import hasRoles, ViCareDeviceAccessor


def has_roles(roles):
    return lambda requested_roles: hasRoles(requested_roles, roles)


class PyViCareDeviceConfigTest(unittest.TestCase):

    def setUp(self) -> None:
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "[device]")
        self.service = Mock()
        self.service.hasRoles = has_roles([])

    def test_autoDetect_Vitodens_asGazBoiler(self):
        c = PyViCareDeviceConfig(self.accessor, self.service, "E3_Vitodens_200_xxxx/E3_Dictionary", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_Unknown_asGeneric(self):
        c = PyViCareDeviceConfig(self.accessor, self.service, "myRobot", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatingDevice", type(device_type).__name__)

    def test_autoDetect_VScot_asGazBoiler(self):
        c = PyViCareDeviceConfig(self.accessor, self.service, "VScotHO1_200", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_RoleBoiler_asGazBoiler(self):
        self.service.hasRoles = has_roles(["type:boiler"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_RoleHeatpump_asHeatpump(self):
        self.service.hasRoles = has_roles(["type:heatpump"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatPump", type(device_type).__name__)

    def test_autoDetect_RoleRadiator_asRadiatorActuator(self):
        self.service.hasRoles = has_roles(["type:radiator"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("RadiatorActuator", type(device_type).__name__)

    def test_autoDetect_RoleClimateSensor_asRoomSensor(self):
        self.service.hasRoles = has_roles(["type:climateSensor"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("RoomSensor", type(device_type).__name__)

    def test_autoDetect_RoleVentilation_asVentilation(self):
        self.service.hasRoles = has_roles(["type:ventilation"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_RoleVentilationCentral_asVentilation(self):
        self.service.hasRoles = has_roles(["type:ventilation;central"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_Vitoair_FS_300F_asVentilation(self):
        c = PyViCareDeviceConfig(self.accessor, self.service, "E3_ViAir_300F", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_RoleVentilationPurifier_asVentilation(self):
        self.service.hasRoles = has_roles(["type:ventilation;purifier"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_Vitopure_350_asVentilation(self):
        c = PyViCareDeviceConfig(self.accessor, self.service, "E3_VitoPure", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_RoleESS_asElectricalEnergySystem(self):
        self.service.hasRoles = has_roles(["type:ess"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("ElectricalEnergySystem", type(device_type).__name__)

    def test_autoDetect_Vitocharge05_asElectricalEnergySystem(self):
        c = PyViCareDeviceConfig(self.accessor, self.service, "E3_VitoCharge_05", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("ElectricalEnergySystem", type(device_type).__name__)

    def test_autoDetect_VitoconnectOpto1_asGateway(self):
        c = PyViCareDeviceConfig(self.accessor, self.service, "Heatbox1", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_VitoconnectOpto2_asGateway(self):
        c = PyViCareDeviceConfig(self.accessor, self.service, "Heatbox2_SRC", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_TCU100_asGateway(self):
        c = PyViCareDeviceConfig(self.accessor, self.service, "E3_TCU41_x04", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_TCU200_asGateway(self):
        c = PyViCareDeviceConfig(self.accessor, self.service, "E3_TCU19_x05", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_TCU300_asGateway(self):
        c = PyViCareDeviceConfig(self.accessor, self.service, "E3_TCU10_x07", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_Ecotronic_asPelletsBoiler(self):
        self.service.hasRoles = has_roles(["type:boiler"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Ecotronic", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("PelletsBoiler", type(device_type).__name__)

    def test_autoDetect_Vitoladens_asOilBoiler(self):
        self.service.hasRoles = has_roles(["type:boiler"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Vitoladens", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("OilBoiler", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway(self):
        self.service.hasRoles = has_roles(["type:gateway;VitoconnectOpto1"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_vc_opto2(self):
        self.service.hasRoles = has_roles(["type:gateway;VitoconnectOpto2/OT2"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_TCU100(self):
        self.service.hasRoles = has_roles(["type:gateway;TCU100"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_TCU200(self):
        self.service.hasRoles = has_roles(["type:gateway;TCU200"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway_TCU300(self):
        self.service.hasRoles = has_roles(["type:gateway;TCU300"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_legacy_device(self):
        self.service.hasRoles = has_roles(["type:legacy"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device = c.asAutoDetectDevice()
        self.assertEqual(device.isLegacyDevice(), True)
        self.assertEqual(device.isE3Device(), False)

    def test_e3_device(self):
        self.service.hasRoles = has_roles(["type:E3"])
        c = PyViCareDeviceConfig(self.accessor, self.service, "Unknown", "Online")
        device = c.asAutoDetectDevice()
        self.assertEqual(device.isLegacyDevice(), False)
        self.assertEqual(device.isE3Device(), True)
