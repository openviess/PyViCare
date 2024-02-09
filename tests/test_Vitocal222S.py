import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
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

    def test_isHeatingDevice(self):
        # "feature": "heating" has "isEnabled: true" but has no property: active: value: true"
        # self.assertTrue(self.device.isHeatingDevice())
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.isHeatingDevice)

    def test_isDomesticHotWaterDevice(self):
        self.assertTrue(self.device.isDomesticHotWaterDevice())

    def test_isSolarThermalDevice(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.isSolarThermalDevice)

    def test_isVentilationDevice(self):
        self.assertTrue(self.device.isVentilationDevice())
