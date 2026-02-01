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

    def test_condenser_getSubcoolingTemperature(self):
        self.assertEqual(self.device.getCondensor("0").getSubcoolingTemperature(), -2.8)
        self.assertEqual(self.device.getCondensor("0").getSubcoolingTemperatureUnit(), "celsius")

    def test_evaporator_getOverheatTemperature(self):
        self.assertEqual(self.device.getEvaporator("0").getOverheatTemperature(), 0.0)
        self.assertEqual(self.device.getEvaporator("0").getOverheatTemperatureUnit(), "celsius")

    def test_evaporator_getLiquidTemperature(self):
        self.assertEqual(self.device.getEvaporator("0").getLiquidTemperature(), 18.2)
        self.assertEqual(self.device.getEvaporator("0").getLiquidTemperatureUnit(), "celsius")

    def test_compressor_getInletPressure(self):
        self.assertEqual(self.device.getCompressor("0").getInletPressure(), 12.9)
        self.assertEqual(self.device.getCompressor("0").getInletPressureUnit(), "bar")
