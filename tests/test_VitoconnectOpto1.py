import unittest

from PyViCare.PyViCareGateway import Gateway
from tests.ViCareServiceMock import ViCareServiceMock

ROLES = [
    "type:gateway;VitoconnectOpto1",
    "type:legacy"
]

class VitoconnectOpto1(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock(ROLES, 'response/VitoconnectOpto1.json')
        self.device = Gateway(self.service)

    def test_isDomesticHotWaterDevice(self):
        self.assertEqual(self.device.isDomesticHotWaterDevice(), False)

    def test_isSolarThermalDevice(self):
        self.assertEqual(self.device.isSolarThermalDevice(), False)

    def test_isVentilationDevice(self):
        self.assertEqual(self.device.isVentilationDevice(), False)

    def test_getSerial(self):
        self.assertEqual(
            self.device.getSerial(), "################")

    def test_getWifiSignalStrength(self):
        self.assertEqual(
            self.device.getWifiSignalStrength(), -69)
