import unittest
from tests.ViCareServiceMockV2 import ViCareServiceMockV2
from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCare import PyViCareNotSupportedFeatureError
import PyViCare.Feature

class Vitocal200V2(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMockV2('response_Vitocal200_V2.json', 0)
        self.heat = HeatPump(None, None, None, 0, 0, self.service)
        PyViCare.Feature.raise_exception_on_not_supported_device_feature = True
        
    def test_getCompressorActive(self):
        self.assertEqual(self.heat.getCompressorActive(), False)

    @unittest.skip("Not available in V2 yet")
    def test_getCompressorHours(self):
        self.assertAlmostEqual(self.heat.getCompressorHours(), 8541)


    @unittest.skip("Not available in V2 yet")
    def test_getHeatingRodStatusOverall(self):
        self.assertEqual(self.heat.getHeatingRodStatusOverall(), False)

    @unittest.skip("Not available in V2 yet")
    def test_getHeatingRodStatusLevel1(self):
        self.assertEqual(self.heat.getHeatingRodStatusLevel1(), False)

    def test_getReturnTemperature(self):
        self.assertAlmostEqual(self.heat.getReturnTemperature(), 27.2)

    @unittest.skip("Not available in V2 yet")
    def test_getMonthSinceLastService_fails(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.heat.getMonthSinceLastService)


    @unittest.skip("Not available in V2 yet")
    def test_getPrograms_fails(self):
        expected_programs = ['active', 'comfort', 'eco', 'fixed', 'normal', 'reduced', 'screedDrying', 'standby']
        self.assertListEqual(self.heat.getPrograms(), expected_programs)

    @unittest.skip("Not available in V2 yet")    
    def test_getModes(self):
        expected_modes = ['standby', 'dhw', 'dhwAndHeatingCooling']
        self.assertListEqual(self.heat.getModes(), expected_modes)
