import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal300G(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "[device]")
        self.service = ViCareServiceMock('response/Vitocal333G.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_getDomesticHotWaterStorageTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterStorageTemperature(), 47.5)

    def test_getHotWaterStorageTemperatureTop(self):
        self.assertEqual(
            self.device.getHotWaterStorageTemperatureTop(), 47.5)

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
