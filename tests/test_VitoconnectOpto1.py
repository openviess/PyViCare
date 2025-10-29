import unittest

from PyViCare.PyViCareGateway import Gateway
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class VitoconnectOpto1(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "gateway")
        self.service = ViCareServiceMock('response/VitoconnectOpto1.json')
        self.device = Gateway(self.accessor, self.service)

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
