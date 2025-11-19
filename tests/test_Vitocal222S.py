import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal222S(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal222S.json')
        self.device = HeatPump(self.service)

    def test_condensers_getLiquidTemperature(self):
        self.assertEqual(self.device.getCondensor(0).getLiquidTemperature(), 26.1)
        self.assertEqual(self.device.getCondensor(0).getLiquidTemperatureUnit(), "celsius")

    def test_compressor_getInletTemperature(self):
        self.assertEqual(self.device.getCompressor(0).getInletTemperature(), 0.0)
        self.assertEqual(self.device.getCompressor(0).getInletTemperatureUnit(), "celsius")

    def test_compressor_getOutletTemperature(self):
        self.assertEqual(self.device.getCompressor(0).getOutletTemperature(), 32.8)
        self.assertEqual(self.device.getCompressor(0).getOutletTemperatureUnit(), "celsius")
