import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal200S(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal200S.json')
        self.device = HeatPump(self.service)

    def test_getDomesticHotWaterConfiguredTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterConfiguredTemperature(), 40)

    def test_getDomesticHotWaterConfiguredTemperature2(self):
        self.assertEqual(
            self.device.getDomesticHotWaterConfiguredTemperature2(), 60)
