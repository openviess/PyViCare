import unittest

from PyViCare.PyViCareGateway import Gateway
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock

ROLES = [
    "capability:hems",
    "capability:zigbeeCoordinator",
    "type:E3",
    "type:gateway;TCU300"
]

class TCU300_ethernet(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock(ROLES, 'response/TCU300_ethernet.json')
        self.device = Gateway(self.service)

    def test_getSerial(self):
        self.assertEqual(
            self.device.getSerial(), "################")

    def test_getWifiSignalStrength(self):
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getWifiSignalStrength()
