import unittest

from PyViCare.PyViCareHeatingDevice import HeatingDevice
from tests.ViCareServiceMock import ViCareServiceMock


class SolarTest(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Solar.json')
        self.device = HeatingDevice(self.service)

    def test_getSolarStorageTemperature(self):
        self.assertEqual(self.device.getSolarStorageTemperature(), 41.5)

    def test_getSolarPowerProduction(self):
        self.assertEqual(
            self.device.getSolarPowerProduction(), [19.773, 20.642, 18.831, 22.672, 18.755, 14.513, 15.406, 13.115])
        self.assertEqual(
            self.device.getSolarPowerProductionDays(), [19.773, 20.642, 18.831, 22.672, 18.755, 14.513, 15.406, 13.115])
        self.assertEqual(
            self.device.getSolarPowerProductionToday(), 19.773)
        self.assertEqual(
            self.device.getSolarPowerProductionWeeks(), [19.773, 20.642, 18.831, 22.672, 18.755, 14.513, 15.406, 13.115])
        self.assertEqual(
            self.device.getSolarPowerProductionThisWeek(), 19.773)
        self.assertEqual(
            self.device.getSolarPowerProductionMonths(), [19.773, 20.642, 18.831, 22.672, 18.755, 14.513, 15.406, 13.115])
        self.assertEqual(
            self.device.getSolarPowerProductionThisMonth(), 19.773)
        self.assertEqual(
            self.device.getSolarPowerProductionYears(), [19.773, 20.642, 18.831, 22.672, 18.755, 14.513, 15.406, 13.115])
        self.assertEqual(
            self.device.getSolarPowerProductionThisYear(), 19.773)

    def test_getSolarCollectorTemperature(self):
        self.assertEqual(self.device.getSolarCollectorTemperature(), 21.9)

    def test_getSolarPumpActive(self):
        self.assertEqual(self.device.getSolarPumpActive(), False)
