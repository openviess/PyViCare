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

    def test_getActiveVentilationMode(self):
        self.assertEqual("sensorDriven", self.device.getActiveVentilationMode())

    def test_getVentilationModes(self):
        expected_modes = ['permanent', 'ventilation', 'sensorDriven']
        self.assertListEqual(expected_modes, self.device.getVentilationModes())

    def test_getVentilationMode(self):
        self.assertEqual(False, self.device.getVentilationMode("filterChange"))

    def test_getVentilationLevels(self):
        expected_levels = ['levelOne', 'levelTwo', 'levelThree', 'levelFour']
        self.assertListEqual(expected_levels, self.device.getVentilationLevels())

    def test_ventilationState(self):
        self.assertEqual(self.device.getVentilationDemand(), "unknown")
        self.assertEqual(self.device.getVentilationLevel(), "unknown")
        self.assertEqual(self.device.getVentilationReason(), "sensorDriven")

    def test_ventilationQuickmode(self):
        self.assertEqual(self.device.getVentilationQuickmode("standby"), False)

    def test_ventilationQuickmodes(self):
        self.assertEqual(self.device.getVentilationQuickmodes(), [
            "forcedLevelFour",
            "standby",
            "silent",
        ])

    def test_activateVentilationQuickmodeStandby(self):
        self.device.activateVentilationQuickmode("standby")
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'activate')
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'ventilation.quickmodes.standby')

    def test_deactivateVentilationQuickmodeStandby(self):
        self.device.deactivateVentilationQuickmode("standby")
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'deactivate')
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'ventilation.quickmodes.standby')
