import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.helper import now_is
from tests.ViCareServiceMock import ViCareServiceMock

ROLES = [
    "capability:backup;0020_HPMU_VC",
    "capability:monetization;AdvancedReport",
    "capability:monetization;DhwSavingsCalculator",
    "type:E3",
    "type:heatpump",
    "type:product;Vitocal_222S"
]

class Vitocal222S(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock(ROLES, 'response/Vitocal222S.json')
        self.device = HeatPump(self.service)

    @unittest.skip("dump is not up to date, dhw modes where changed for E3 devices in 2023")
    def test_getDomesticHotWaterActiveMode_10_10_time(self):
        with now_is('2000-01-01 10:10:00'):
            self.assertEqual(
                self.device.getDomesticHotWaterActiveMode(), 'normal')

    def test_getCurrentDesiredTemperature(self):
        self.assertEqual(
            self.device.circuits[0].getCurrentDesiredTemperature(), 23)
