import unittest
from unittest.mock import patch

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Compressor(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")

    def test_getSpeed_preserves_fractional_values(self):
        for model, expected in (("Vitocal250A", 0.0), ("Vitocal252A", 38.5)):
            with self.subTest(model=model):
                service = ViCareServiceMock(f"response/{model}.json")
                device = HeatPump(self.accessor, service)
                speed = device.getCompressor(0).getSpeed()
                self.assertEqual(speed, expected)
                self.assertIsInstance(speed, float)

    def test_temperatures_not_connected(self):
        service = ViCareServiceMock("response/Vitocal222S.json")
        compressor = HeatPump(self.accessor, service).getCompressor(0)
        not_connected = {"properties": {"status": {"value": "notConnected"}}}
        for method in (compressor.getMotorChamberTemperature,
                       compressor.getAmbientTemperature,
                       compressor.getOverheatTemperature):
            with self.subTest(method=method), patch.object(compressor, "getProperty", return_value=not_connected):
                self.assertRaises(PyViCareNotSupportedFeatureError, method)
