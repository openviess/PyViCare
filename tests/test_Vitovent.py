import unittest

from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from PyViCare.PyViCareVentilationDevice import VentilationDevice
from tests.ViCareServiceMock import ViCareServiceMock


class Vitovent(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitovent.json')
        self.device = VentilationDevice(self.service)

    def test_isHeatingDevice(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.isHeatingDevice)

    def test_isDomesticHotWaterDevice(self):
        self.assertTrue(self.device.isDomesticHotWaterDevice())

    def test_isSolarThermalDevice(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.isSolarThermalDevice)

    def test_isVentilationDevice(self):
        self.assertTrue(self.device.isVentilationDevice())
