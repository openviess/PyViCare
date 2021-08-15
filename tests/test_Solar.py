import unittest

from PyViCare.PyViCareDevice import Device
from tests.ViCareServiceMock import ViCareServiceMock


class SolarTest(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Solar.json')
        self.device = Device(self.service)

    def test_getSolarStorageTemperature(self):
        self.assertEqual(self.device.getSolarStorageTemperature(), 63.5)

    def test_getSolarPowerProduction(self):
        self.assertEqual(
            self.device.getSolarPowerProduction(), [16.604, 19.78, 19.323, 20.592, 19.444, 14.517, 17.929, 20.534])
