import unittest

from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from PyViCare.PyViCareVentilationDevice import VentilationDevice
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal200(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal111S.json')
        self.device = VentilationDevice(self.service)

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
