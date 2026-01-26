import unittest

from PyViCare.PyViCareVentilationDevice import VentilationDevice
from tests.ViCareServiceMock import ViCareServiceMock


class VitoairFs300(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/VitoairFs300E.json')
        self.device = VentilationDevice(self.service)

    def test_isDomesticHotWaterDevice(self):
        self.assertEqual(self.device.isDomesticHotWaterDevice(), False)

    def test_isSolarThermalDevice(self):
        self.assertEqual(self.device.isSolarThermalDevice(), False)

    def test_isVentilationDevice(self):
        self.assertEqual(self.device.isVentilationDevice(), True)

    def test_getActiveVentilationMode(self):
        self.assertEqual(self.device.getActiveVentilationMode(), "sensorOverride")

    def test_getActiveVentilationProgram(self):
        self.assertEqual(self.device.getActiveVentilationProgram(), "levelFour")

    def test_getVentilationModes(self):
        expected_modes = ['permanent', 'ventilation', 'sensorOverride', 'sensorDriven']
        self.assertListEqual(self.device.getVentilationModes(), expected_modes)

    def test_getVentilationPrograms(self):
        expected_programs = ['standby']
        self.assertListEqual(self.device.getVentilationPrograms(), expected_programs)

    def test_getVentilationLevels(self):
        expected_levels = ['levelOne', 'levelTwo', 'levelThree', 'levelFour']
        self.assertListEqual(expected_levels, self.device.getVentilationLevels())

    def test_getVentilationSchedule(self):
        keys = ['active', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        self.assertListEqual(list(self.device.getVentilationSchedule().keys()), keys)

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), "################")

    def test_getVentilationMode(self):
        self.assertEqual(False, self.device.getVentilationMode("filterChange"))

    def test_ventilationQuickmode(self):
        self.assertEqual(self.device.getVentilationQuickmode("forcedLevelFour"), False)
        self.assertEqual(self.device.getVentilationQuickmode("silent"), False)

    def test_ventilationQuickmodes(self):
        self.assertEqual(self.device.getVentilationQuickmodes(), [
            "forcedLevelFour",
            "silent",
        ])

    def test_getExhaustTemperature(self):
        self.assertEqual(self.device.getExhaustTemperature(), 18.5)

    def test_getExtractTemperature(self):
        self.assertEqual(self.device.getExtractTemperature(), 21.2)

    def test_getExhaustHumidity(self):
        self.assertEqual(self.device.getExhaustHumidity(), 78)

    def test_getExtractHumidity(self):
        self.assertEqual(self.device.getExtractHumidity(), 55)

    def test_getHeatRecoveryEfficiency(self):
        self.assertEqual(self.device.getHeatRecoveryEfficiency(), 87.5)
