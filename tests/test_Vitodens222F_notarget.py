import unittest
from tests.ViCareServiceMock import ViCareServiceMock
from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCare import PyViCareNotSupportedFeatureError
import PyViCare.Feature

class Vitodens222F_NoTarget(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response_Vitodens222F_notarget.json', 0)
        self.gaz = GazBoiler(None, None, None, 0, 0, self.service)
        PyViCare.Feature.raise_exception_on_not_supported_device_feature = True

    def test_getTargetSupplyTemperature(self):
        self.assertAlmostEqual(self.gaz.getTargetSupplyTemperature(), None)
        
