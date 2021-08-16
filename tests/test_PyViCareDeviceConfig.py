import unittest

from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig


class PyViCareDeviceConfigTest(unittest.TestCase):

    def test_autoDetect_Vitodens_asGazBoiler(self):
        c = PyViCareDeviceConfig(
            None, "E3_Vitodens_200_xxxx/E3_Dictionary", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)

    def test_autoDetect_Unknown_asGeneric(self):
        c = PyViCareDeviceConfig(None, "myRobot", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("Device", type(device_type).__name__)

    def test_autoDetect_VScot_asGazBoiler(self):
        c = PyViCareDeviceConfig(None, "VScotHO1_200", "Online")
        device_type = c.asAutoDetectDevice()
        self.assertEqual("GazBoiler", type(device_type).__name__)
