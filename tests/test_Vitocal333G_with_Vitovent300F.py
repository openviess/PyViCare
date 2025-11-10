import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal333G_with_Vitovent300F(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal333G-with-Vitovent300F.json')
        self.device = HeatPump(self.service)

    def test_getHeatExchangerFrostProtectionActive(self):
        self.assertFalse(self.device.getHeatExchangerFrostProtectionActive())

    def test_getVolumeFlow(self):
        self.assertEqual(self.device.getSupplyVolumeFlow(), 257)
        self.assertEqual(self.device.getExhaustVolumeFlow(), 257)
