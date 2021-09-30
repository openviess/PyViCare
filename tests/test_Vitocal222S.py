import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.helper import now_is
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal222S(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal222S.json')
        self.device = HeatPump(self.service)

    def test_getDomesticHotWaterActiveMode_10_10_time(self):
        with now_is('2000-01-01 10:10:00'):
            self.assertEqual(
                self.device.getDomesticHotWaterActiveMode(), 'normal')

    def test_getCurrentDesiredTemperature(self):
        self.assertEqual(
            self.device.circuits[0].getCurrentDesiredTemperature(), 23)
