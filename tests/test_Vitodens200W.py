import unittest
from tests.ViCareServiceMock import ViCareServiceMock
from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCare import PyViCareNotSupportedFeatureError
import PyViCare.Feature

class Vitodens200W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response_Vitodens200W.json', 0)
        self.device = GazBoiler(None, None, None, 0, 0, self.service)
        PyViCare.Feature.raise_exception_on_not_supported_device_feature = True

    def test_getBurnerActive(self):
        self.assertEqual(self.device.getBurnerActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.getBurnerStarts(), 17169)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.getBurnerHours(), 1589.3)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.getBurnerModulation(), 0)

    def test_getPowerConsumptionDays_fails(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.getPowerConsumptionDays)

    def test_getPrograms(self):
        expected_programs = ['active', 'comfort', 'eco', 'external', 'holiday', 'normal', 'reduced', 'standby']
        self.assertListEqual(self.device.getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['standby', 'dhw', 'dhwAndHeating', 'forcedReduced', 'forcedNormal']
        self.assertListEqual(self.device.getModes(), expected_modes)

    def test_getPrograms(self):
        expected_modes = ['active', 'comfort', 'eco', 'external', 'holiday', 'normal', 'reduced', 'standby']
        self.assertListEqual(self.device.getPrograms(), expected_modes)

    def test_ensure_old_behavior_non_supported_feature_returns_error(self):
        PyViCare.Feature.raise_exception_on_not_supported_device_feature = False
        self.assertEqual(self.device.getPowerConsumptionDays(), "error")

    def test_getFrostProtectionActive(self):
        self.assertEqual(self.device.getFrostProtectionActive(), False)
