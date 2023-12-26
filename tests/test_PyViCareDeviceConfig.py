import unittest
from unittest.mock import Mock

from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareService import hasRoles


def has_roles(roles):
    return lambda requested_roles: hasRoles(requested_roles, roles)


class PyViCareDeviceConfigTest(unittest.TestCase):

    def setUp(self) -> None:
        self.service = Mock()
        self.service.hasRoles = has_roles([])

    def test_autoDetect_Vitodens_asGazBoiler(self):
        c = PyViCareDeviceConfig(
            self.service, "0", "E3_Vitodens_200_xxxx/E3_Dictionary", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_Unknown_asGeneric(self):
        c = PyViCareDeviceConfig(self.service, "0", "myRobot", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatingDevice", type(device_type).__name__)

    def test_autoDetect_VScot_asGazBoiler(self):
        c = PyViCareDeviceConfig(self.service, "0", "VScotHO1_200", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_RoleBoiler_asGazBoiler(self):
        self.service.hasRoles = has_roles(["type:boiler"])
        c = PyViCareDeviceConfig(self.service, "0", "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_RoleHeatpump_asHeatpump(self):
        self.service.hasRoles = has_roles(["type:heatpump"])
        c = PyViCareDeviceConfig(self.service, "0", "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatPump", type(device_type).__name__)

    def test_autoDetect_RoleRadiator_asRadiatorActuator(self):
        self.service.hasRoles = has_roles(["type:radiator"])
        c = PyViCareDeviceConfig(self.service, "0", "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("RadiatorActuator", type(device_type).__name__)

    def test_autoDetect_RoleClimateSensor_asRoomSensor(self):
        self.service.hasRoles = has_roles(["type:climateSensor"])
        c = PyViCareDeviceConfig(self.service, "0", "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("RoomSensor", type(device_type).__name__)

    def test_autoDetect_RoleVentilation_asVentilation(self):
        self.service.hasRoles = has_roles(["type:ventilation"])
        c = PyViCareDeviceConfig(self.service, "0", "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_Vitoair_FS_300E_asVentilation(self):
        # self.service.hasRoles = has_roles(["type:ventilation"])
        c = PyViCareDeviceConfig(self.service, "0", "E3_ViAir_300F", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("VentilationDevice", type(device_type).__name__)

    def test_autoDetect_VitoconnectOpto1_asGateway(self):
        c = PyViCareDeviceConfig(self.service, "0", "Heatbox1", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)

    def test_autoDetect_RoleGateway_asGateway(self):
        self.service.hasRoles = has_roles(["type:gateway;VitoconnectOpto1"])
        c = PyViCareDeviceConfig(self.service, "0", "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Gateway", type(device_type).__name__)
