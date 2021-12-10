import unittest

from PyViCare.PyViCareOilBoiler import OilBoiler
from tests.ViCareServiceMock import ViCareServiceMock


class VitolaUniferral(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/VitolaUniferral.json')
        self.device = OilBoiler(self.service)

    def test_getDomesticHotWaterConfiguredTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterConfiguredTemperature(), 60)

    def test_getActive(self):
        self.assertEqual(self.device.burners[0].getActive(), True)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.burners[0].getStarts(), 5156)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.burners[0].getHours(), 1021.4)

    def test_getBoilerTemperature(self):
        self.assertEqual(self.device.getBoilerTemperature(), 26.6)

    def test_getDomesticHotWaterStorageTemperature(self):
        self.assertEqual(self.device.getDomesticHotWaterStorageTemperature(), 56.9)
