import unittest

from PyViCare.PyViCareGateway import Gateway
from tests.ViCareServiceMock import ViCareServiceMock


class VitoconnectOpto1(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/VitoconnectOpto1.json')
        self.device = Gateway(self.service)

    def test_getWifiSignalStrength(self):
        self.assertEqual(
            self.device.getWifiSignalStrength(), -69)
