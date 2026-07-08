import unittest

from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareGateway import Gateway
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class TCU300_ethernet(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/TCU300_ethernet.json')
        self.device = Gateway(self.accessor, self.service)

    def test_getSerial(self):
        self.assertEqual(
            self.device.getSerial(), "################")

    def test_getWifiSignalStrength(self):
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getWifiSignalStrength()
