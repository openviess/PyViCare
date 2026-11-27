import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal262A(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/Vitocal262A_T2H-R290.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_getSeasonalPerformanceFactor(self):
        self.assertEqual(self.device.getSeasonalPerformanceFactorDHW(), 2.8)
        self.assertEqual(self.device.getSeasonalPerformanceFactorHeating(), 0.0)
        self.assertEqual(self.device.getSeasonalPerformanceFactorTotal(), 2.8)

    def test_getDomesticHotWaterHysteresis(self):
        self.assertEqual(self.device.getDomesticHotWaterHysteresis(), 7.0)
        self.assertEqual(self.device.getDomesticHotWaterHysteresisSwitchOn(), 7.0)
        self.assertEqual(self.device.getDomesticHotWaterHysteresisSwitchOff(), 0.0)

    def test_getEvaporatorLiquidTemperature(self):
        self.assertEqual(self.device.evaporators[0].getLiquidTemperature(), 25.3)

    def test_getDomesticHotWaterHygiene(self):
        self.assertTrue(self.device.getDomesticHotWaterHygieneEnabled())
        self.assertFalse(self.device.getDomesticHotWaterHygieneActive())
        self.assertEqual(self.device.getDomesticHotWaterHygieneTemperature(), 60)
        self.assertEqual(self.device.getDomesticHotWaterHygieneTriggerStartHour(), 12)
        self.assertEqual(self.device.getDomesticHotWaterHygieneTriggerStartMinute(), 0)
        self.assertEqual(self.device.getDomesticHotWaterHygieneTriggerWeekdays(), ["Tue"])
