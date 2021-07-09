from PyViCare.PyViCareServiceV2 import ViCareServiceV2
import unittest
from tests.ViCareServiceMockV2 import ViCareServiceMockV2
from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCare import PyViCareNotSupportedFeatureError
import PyViCare.Feature

class Vitodens200WV2(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMockV2('response_Vitodens200W_V2.json', 0)
        self.gaz = GazBoiler(None, None, None, 0, 0, self.service)
        PyViCare.Feature.raise_exception_on_not_supported_device_feature = True
        
    def test_getBurnerActive(self):
        self.assertEqual(self.gaz.getBurnerActive(), False)

    @unittest.skip("Not available in V2 yet")
    def test_getBurnerStarts(self):
        self.assertEqual(self.gaz.getBurnerStarts(), 12648)

    def test_getPowerConsumptionDays_fails(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.gaz.getPowerConsumptionDays)

    def test_getMonthSinceLastService_fails(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.gaz.getMonthSinceLastService)

    def test_getPrograms_fails(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.gaz.getPrograms)
    
    @unittest.skip("Not available in V2 yet")
    def test_getModes(self):
        expected_modes = ['standby', 'dhw', 'dhwAndHeating']
        self.assertListEqual(self.gaz.getModes(), expected_modes)
        self.assertRaises(PyViCareNotSupportedFeatureError, self.gaz.getPrograms)

    def test_ensure_old_behavior_non_supported_feature_returns_error(self):
        PyViCare.Feature.raise_exception_on_not_supported_device_feature = False
        self.assertEqual(self.gaz.getPowerConsumptionDays(), "error")