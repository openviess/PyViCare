import unittest

from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal200(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/Vitocal111S.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_ventilation_state(self):
        self.assertEqual(self.device.getVentilationDemand(), "ventilation")
        self.assertEqual(self.device.getVentilationLevel(), "levelOne")
        self.assertEqual(self.device.getVentilationReason(), "schedule")

    def test_ventilationQuickmode(self):
        # quickmodes disabled
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getVentilationQuickmode("comfort")
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getVentilationQuickmode("eco")
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getVentilationQuickmode("holiday")

    def test_ventilationQuickmodes(self):
        self.assertEqual(self.device.getVentilationQuickmodes(), [
            "comfort",
            "eco",
            "holiday",
        ])
