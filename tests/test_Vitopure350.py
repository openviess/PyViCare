import unittest

from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from PyViCare.PyViCareVentilationDevice import VentilationDevice
from tests.ViCareServiceMock import ViCareServiceMock


class Vitopure350(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitopure350.json')
        self.device = VentilationDevice(self.service)

    def test_getActiveMode(self):
        self.assertEqual("sensorDriven", self.device.getActiveMode())

    def test_getAvailableModes(self):
        expected_modes = ['permanent', 'ventilation', 'sensorDriven']
        self.assertListEqual(expected_modes, self.device.getAvailableModes())

    def test_getActiveProgram(self):
        self.assertEqual("automatic", self.device.getActiveProgram())

    def test_getAvailablePrograms(self):
        expected_programs = ['standby']
        self.assertListEqual(expected_programs, self.device.getAvailablePrograms())

    def test_getPermanentLevels(self):
        expected_levels = ['levelOne', 'levelTwo', 'levelThree', 'levelFour']
        self.assertListEqual(expected_levels, self.device.getPermanentLevels())

    def test_getSchedule(self):
        keys = ['active', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        self.assertListEqual(keys, list(self.device.getSchedule().keys()))

    def test_getSerial(self):
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getSerial()

    def test_ventilationState(self):
        self.assertEqual(self.device.getVentilationDemand(), "unknown")
        self.assertEqual(self.device.getVentilationLevel(), "unknown")
        self.assertEqual(self.device.getVentilationReason(), "sensorDriven")
