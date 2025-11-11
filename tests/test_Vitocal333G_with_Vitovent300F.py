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

    def test_getCondensorSubcoolingTemperature(self):
        self.assertEqual(self.device.getCondensor("0").getCondensorSubcoolingTemperature(), -2.8)
        self.assertEqual(self.device.getCondensor("0").getCondensorSubcoolingTemperatureUnit(), "celsius")

    def test_getEvaporatorOverheatTemperature(self):
        self.assertEqual(self.device.getEvaporator("0").getEvaporatorOverheatTemperature(), 0.0)
        self.assertEqual(self.device.getEvaporator("0").getEvaporatorOverheatTemperatureUnit(), "celsius")
