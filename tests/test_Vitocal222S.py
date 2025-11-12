import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal222S(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal222S.json')
        self.device = HeatPump(self.service)

    def test_getCondensorsLiquidTemperature(self):
        self.assertEqual(self.device.getCondensor(0).getCondensorLiquidTemperature(), 26.1)
        self.assertEqual(self.device.getCondensor(0).getCondensorLiquidTemperatureUnit(), "celsius")

    def test_getCompressorInletTemperature(self):
        self.assertEqual(self.device.getCompressor(0).getCompressorInletTemperature(), 0.0)
        self.assertEqual(self.device.getCompressor(0).getCompressorInletTemperatureUnit(), "celsius")

    def test_getCompressorOutletTemperature(self):
        self.assertEqual(self.device.getCompressor(0).getCompressorOutletTemperature(), 32.8)
        self.assertEqual(self.device.getCompressor(0).getCompressorOutletTemperatureUnit(), "celsius")

    def test_getCompressorSpeed(self):
        self.assertEqual(self.device.getCompressor(0).getSpeed(), 20)
