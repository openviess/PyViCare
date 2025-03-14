import unittest

from PyViCare.PyViCareGateway import Gateway
from tests.ViCareServiceMock import ViCareServiceMock

ROLES = [
    "type:gateway;VitoconnectOpto2/OT2",
    "type:hb2",
    "type:legacy"
]

class VitoconnectOpto2(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock(ROLES, 'response/VitoconnectOpto2.json')
        self.device = Gateway(self.service)

    def test_getSerial(self):
        self.assertEqual(
            self.device.getSerial(), "##############")

    def test_getWifiSignalStrength(self):
        self.assertEqual(
            self.device.getWifiSignalStrength(), -41)
