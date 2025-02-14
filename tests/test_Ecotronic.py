import unittest

from PyViCare.PyViCarePelletsBoiler import PelletsBoiler
from tests.ViCareServiceMock import ViCareServiceMock


class Ecotronic(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Ecotronic.json')
        self.device = PelletsBoiler(self.service)

    def test_isDomesticHotWaterDevice(self):
        self.assertEqual(self.device.isDomesticHotWaterDevice(), False)

    def test_isSolarThermalDevice(self):
        self.assertEqual(self.device.isSolarThermalDevice(), False)

    def test_isVentilationDevice(self):
        self.assertEqual(self.device.isVentilationDevice(), False)

    @unittest.skip("burners broken")
    def test_getBurnerStarts(self):
        self.assertEqual(self.device.burners[0].getStarts(), 2162)

    @unittest.skip("burners broken")
    def test_getBurnerHours(self):
        self.assertEqual(self.device.burners[0].getHours(), 5648)

    @unittest.skip("burners broken")
    def test_getBurnerModulation(self):
        self.assertEqual(self.device.burners[0].getModulation(), 0)

    @unittest.skip("burners broken")
    def test_getActive(self):
        self.assertEqual(self.device.burners[0].getActive(), False)

    def test_getReturnTemperature(self):
        self.assertEqual(
            self.device.getReturnTemperature(), 60.3)

    def test_getFuelNeed(self):
        self.assertEqual(self.device.getFuelNeed(), 17402)

    def test_getAshLevel(self):
        self.assertEqual(self.device.getAshLevel(), 43.7)
