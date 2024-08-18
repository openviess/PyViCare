import unittest

from PyViCare.PyViCareOilBoiler import OilBoiler
from tests.ViCareServiceMock import ViCareServiceMock


class Vitoladens300C(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitoladens300-C_J3RA.json')
        self.device = OilBoiler(self.service)

    def test_getActive(self):
        self.assertEqual(self.device.burners[0].getActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.burners[0].getStarts(), 29494)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.burners[0].getHours(), 4272)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.burners[0].getModulation(), 0)

    def test_getBoilerTemperature(self):
        self.assertEqual(self.device.getBoilerTemperature(), 26)

    def test_getDomesticHotWaterStorageTemperature(self):
        self.assertEqual(self.device.getDomesticHotWaterStorageTemperature(), 60.8)
