import unittest

from PyViCare.PyViCareGateway import Gateway
from tests.ViCareServiceMock import ViCareServiceMock


class VitoconnectOpto2(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/VitoconnectOpto2.json')
        self.device = Gateway(self.service)

    def test_getSerial(self):
        self.assertEqual(
            self.device.getSerial(), "##############")

    def test_getWifiSignalStrength(self):
        self.assertEqual(
            self.device.getWifiSignalStrength(), -41)
