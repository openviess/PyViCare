import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.helper import now_is
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal222S(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "[device]")
        self.service = ViCareServiceMock('response/Vitocal222S.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_getDomesticHotWaterActiveMode_10_10_time(self):
        with now_is('2000-01-01 10:10:00'):
            self.assertEqual(
                self.device.getDomesticHotWaterActiveMode(), 'normal')

    def test_getCurrentDesiredTemperature(self):
        self.assertEqual(
            self.device.circuits[0].getCurrentDesiredTemperature(), 23)

    def test_isDomesticHotWaterDevice(self):
        self.assertEqual(self.device.isDomesticHotWaterDevice(), True)

    def test_isSolarThermalDevice(self):
        self.assertEqual(self.device.isSolarThermalDevice(), False)

    def test_isVentilationDevice(self):
        self.assertEqual(self.device.isVentilationDevice(), True)

    def test_getActiveVentilationMode(self):
        self.assertEqual("ventilation", self.device.getActiveVentilationMode())

    def test_getVentilationModes(self):
        expected_modes = ['standby', 'standard', 'ventilation']
        self.assertListEqual(expected_modes, self.device.getVentilationModes())

    def test_getVentilationMode(self):
        self.assertEqual(False, self.device.getVentilationMode("standby"))

    def test_ventilationState(self):
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getVentilationDemand()
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getVentilationLevel()
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getVentilationReason()

    def test_ventilationQuickmode(self):
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getVentilationQuickmode("standby")

    def test_ventilationQuickmodes(self):
        self.assertEqual(self.device.getVentilationQuickmodes(), [])
