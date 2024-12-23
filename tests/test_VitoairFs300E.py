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

    def test_getActiveMode(self):
        self.assertEqual(self.device.getActiveMode(), "sensorOverride")

    def test_getActiveProgram(self):
        self.assertEqual(self.device.getActiveProgram(), "levelFour")

    def test_getAvailableModes(self):
        expected_modes = ['permanent', 'ventilation', 'sensorOverride', 'sensorDriven']
        self.assertListEqual(self.device.getAvailableModes(), expected_modes)

    def test_getAvailablePrograms(self):
        expected_programs = ['standby']
        self.assertListEqual(self.device.getAvailablePrograms(), expected_programs)

    def test_getPermanentLevels(self):
        expected_levels = ['levelOne', 'levelTwo', 'levelThree', 'levelFour']
        self.assertListEqual(expected_levels, self.device.getPermanentLevels())

    def test_getSchedule(self):
        keys = ['active', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        self.assertListEqual(list(self.device.getSchedule().keys()), keys)

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), "################")

    def test_getActiveVentilationMode(self):
        self.assertEqual("sensorOverride", self.device.getActiveVentilationMode())

    def test_getVentilationModes(self):
        expected_modes = ['permanent', 'ventilation', 'sensorOverride', 'sensorDriven']
        self.assertListEqual(expected_modes, self.device.getVentilationModes())

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
