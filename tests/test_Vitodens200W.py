import unittest
from tests.ViCareServiceMock import ViCareServiceMock
from PyViCare.PyViCareGazBoiler import GazBoiler
import PyViCare.Feature

class Vitodens200W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response_Vitodens200W.json', 0)
        self.device = GazBoiler(self.service)
        PyViCare.Feature.raise_exception_on_not_supported_device_feature = True

    def test_getBurnerActive(self):
        self.assertEqual(self.device.getBurnerActive(), True)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.getBurnerStarts(), 8028)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.getBurnerHours(), 5570)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.getBurnerModulation(), 11.1)

    def test_getPrograms(self):
        expected_programs = ['active', 'comfort', 'forcedLastFromSchedule', 'normal', 'reduced', 'standby']
        self.assertListEqual(self.device.getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes =  ['standby', 'heating', 'dhw', 'dhwAndHeating']
        self.assertListEqual(self.device.getModes(), expected_modes)

    def test_getPowerConsumptionDays(self):
        expected_consumption = [0, 0.1, 0.2, 0.1, 0.2, 0.2, 0.2, 0.2]
        self.assertEqual(self.device.getPowerConsumptionDays(), expected_consumption)

    def test_getFrostProtectionActive(self):
        self.assertEqual(self.device.getFrostProtectionActive(), False)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(self.device.getDomesticHotWaterCirculationPumpActive(), True)
