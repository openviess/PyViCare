import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal_with_Vitovent(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "[device]")
        self.service = ViCareServiceMock('response/Vitocal-200S-with-Vitovent-300W.json')
        self.device = HeatPump(self.accessor, self.service)

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

    def test_ventilation_state(self):
        self.assertEqual(self.device.getVentilationDemand(), "ventilation")
        self.assertEqual(self.device.getVentilationLevel(), "levelTwo")
        self.assertEqual(self.device.getVentilationReason(), "schedule")

    def test_ventilationQuickmode(self):
        self.assertEqual(self.device.getVentilationQuickmode("comfort"), False)
        self.assertEqual(self.device.getVentilationQuickmode("eco"), False)
        self.assertEqual(self.device.getVentilationQuickmode("holiday"), False)

    def test_ventilationQuickmodes(self):
        self.assertEqual(self.device.getVentilationQuickmodes(), [
            "comfort",
            "eco",
            "holiday",
        ])
