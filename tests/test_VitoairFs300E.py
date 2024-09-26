import unittest

from PyViCare.PyViCareVentilationDevice import VentilationDevice
from tests.ViCareServiceMock import ViCareServiceMock


class VitoairFs300(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/VitoairFs300E.json')
        self.device = VentilationDevice(self.service)

    def test_getActiveMode(self):
        self.assertEqual(self.device.getActiveMode(), "permanent")

    def test_getActiveProgram(self):
        self.assertEqual(self.device.getActiveProgram(), "levelOne")

    def test_getAvailableModes(self):
        expected_modes = ['permanent', 'ventilation', 'sensorOverride', 'sensorDriven']
        self.assertListEqual(self.device.getAvailableModes(), expected_modes)

    def test_getAvailablePrograms(self):
        expected_programs = ['standby']
        self.assertListEqual(self.device.getAvailablePrograms(), expected_programs)

    def test_getSchedule(self):
        keys = ['active', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        self.assertListEqual(list(self.device.getSchedule().keys()), keys)

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), "################")
