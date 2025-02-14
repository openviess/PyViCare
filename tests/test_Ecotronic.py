import unittest

from PyViCare.PyViCarePelletsBoiler import PelletsBoiler
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
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

    def test_getBufferTopTemperature(self):
        self.assertEqual(self.device.getBufferTopTemperature(), 62.1)

    def test_getBufferMidTopTemperature(self):
        self.assertEqual(self.device.getBufferMidTopTemperature(), 50.7)

    def test_getBufferMiddleTemperature(self):
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getBufferMiddleTemperature()

    def test_getBufferMidBottomTemperature(self):
        self.assertEqual(self.device.getBufferMidBottomTemperature(), 44.6)

    def test_getBufferBottomTemperature(self):
        self.assertEqual(self.device.getBufferBottomTemperature(), 43.7)

    def test_getFuelNeed(self):
        self.assertEqual(self.device.getFuelNeed(), 17402)

    def test_getFuelUnit(self):
        self.assertEqual(self.device.getFuelUnit(), "kg")

    def test_getAshLevel(self):
        self.assertEqual(self.device.getAshLevel(), 43.7)
