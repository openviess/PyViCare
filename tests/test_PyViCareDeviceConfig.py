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
            self.service, "E3_Vitodens_200_xxxx/E3_Dictionary", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_Unknown_asGeneric(self):
        c = PyViCareDeviceConfig(self.service, "myRobot", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Device", type(device_type).__name__)

    def test_autoDetect_VScot_asGazBoiler(self):
        c = PyViCareDeviceConfig(self.service, "VScotHO1_200", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_RoleBoiler_asGazBoiler(self):
        self.service.hasRoles = has_roles(["type:boiler"])
        c = PyViCareDeviceConfig(self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_RoleHeatpump_asHeatpump(self):
        self.service.hasRoles = has_roles(["type:heatpump"])
        c = PyViCareDeviceConfig(self.service, "Unknown", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("HeatPump", type(device_type).__name__)
