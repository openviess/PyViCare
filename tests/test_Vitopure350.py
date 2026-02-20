import unittest

from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from PyViCare.PyViCareVentilationDevice import VentilationDevice
from tests.ViCareServiceMock import ViCareServiceMock


class Vitopure350(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitopure350.json')
        self.device = VentilationDevice(self.service)

    def test_getActiveVentilationMode(self):
        self.assertEqual("sensorDriven", self.device.getActiveVentilationMode())

    def test_getVentilationModes(self):
        expected_modes = ['permanent', 'ventilation', 'sensorDriven']
        self.assertListEqual(expected_modes, self.device.getVentilationModes())

    def test_getActiveVentilationProgram(self):
        self.assertEqual("levelTwo", self.device.getActiveVentilationProgram())

    def test_getVentilationPrograms(self):
        expected_programs = []
        self.assertListEqual(expected_programs, self.device.getVentilationPrograms())

    def test_getVentilationLevels(self):
        expected_levels = ['levelOne', 'levelTwo', 'levelThree', 'levelFour']
        self.assertListEqual(expected_levels, self.device.getVentilationLevels())

    def test_getVentilationSchedule(self):
        keys = ['active', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        self.assertListEqual(keys, list(self.device.getVentilationSchedule().keys()))

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), '################')

    def test_getVentilationMode(self):
        self.assertEqual(False, self.device.getVentilationMode("filterChange"))

    def test_ventilationState(self):
        self.assertEqual(self.device.getVentilationDemand(), "unknown")
        self.assertEqual(self.device.getVentilationLevel(), "unknown")
        self.assertEqual(self.device.getVentilationReason(), "standby")

    def test_ventilationQuickmode(self):
        self.assertEqual(self.device.getVentilationQuickmode("standby"), True)

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

    @unittest.skip("testdata missing")
    def test_getOutsideTemperature(self):
        self.assertEqual(self.device.getOutsideTemperature(), 15.0)
        self.assertEqual(self.device.getOutsideHumidity(), 15)

    def test_getSupplyTemperature(self):
        self.assertEqual(self.device.getSupplyTemperature(), 20.7)
        self.assertEqual(self.device.getSupplyHumidity(), 43)

    def test_getVolatileOrganicCompounds(self):
        self.assertEqual(self.device.getVolatileOrganicCompounds(), 68)

    def test_getSupplyFanSpeed(self):
        self.assertEqual(self.device.getSupplyFanSpeed(), 1181)
        self.assertEqual(self.device.getSupplyFanTargetSpeed(), 1181)
        self.assertEqual(self.device.getSupplyFanHours(), 1171)

    def test_getFilterHours(self):
        self.assertEqual(self.device.getFilterHours(), 6994)
        self.assertEqual(self.device.getFilterRemainingHours(), 1766)
        self.assertEqual(self.device.getFilterOverdueHours(), 0)

    def test_getAirborneDust(self):
        self.assertEqual(self.device.getAirborneDustPM1(), 0.3)
        self.assertEqual(self.device.getAirborneDustPM2d5(), 0.3)
        self.assertEqual(self.device.getAirborneDustPM4(), 0.3)
        self.assertEqual(self.device.getAirborneDustPM10(), 0.3)

    def test_getWifiSignalStrength(self):
        self.assertEqual(self.device.getWifiSignalStrength(), -61)
