import unittest

from PyViCare.PyViCareVentilationDevice import VentilationDevice
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal_with_Vitovent(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal-200S-with-Vitovent-300W.json')
        self.device = VentilationDevice(self.service)

    def test_isDomesticHotWaterDevice(self):
        self.assertEqual(self.device.isDomesticHotWaterDevice(), True)

    def test_isSolarThermalDevice(self):
        self.assertEqual(self.device.isSolarThermalDevice(), False)

    def test_isVentilationDevice(self):
        self.assertEqual(self.device.isVentilationDevice(), True)

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
