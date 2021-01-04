import unittest
from tests.ViCareServiceForTesting import ViCareServiceForTesting
from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCare import PyViCareNotSupportedFeatureError
import PyViCare.Feature

class Vitodens111W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceForTesting('response_Vitocal200.json', 0)
        self.heat = HeatPump(None, None, None, 0, 0, self.service)
        PyViCare.Feature.raise_exception_on_not_supported_device_feature = True
        
    def test_getCompressorActive(self):
        self.assertEqual(self.heat.getCompressorActive(), False)

    def test_getCompressorHours(self):
        self.assertAlmostEqual(self.heat.getCompressorHours(), 6801.2)

    def test_getHeatingRodStatusOverall(self):
        self.assertEqual(self.heat.getHeatingRodStatusOverall(), False)

    def test_getHeatingRodStatusLevel1(self):
        self.assertEqual(self.heat.getHeatingRodStatusLevel1(), False)

    def test_getSuctionGasPressure(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.heat.getSuctionGasPressure)
        
    def test_getHotGasPressure(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.heat.getHotGasPressure)

    def test_getReturnTemperature(self):
        self.assertAlmostEqual(self.heat.getReturnTemperature(), 25.8)

    def test_getExpansionValve(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.heat.getExpansionValve)
        
    def test_getCompressorPower_fails(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.heat.getCompressorPower)

    def test_getMonthSinceLastService_fails(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.heat.getMonthSinceLastService)

    def test_getPrograms_fails(self):
        expected_programs = ['active', 'comfort', 'eco', 'fixed', 'holiday', 'normal', 'reduced', 'standby']
        self.assertListEqual(self.heat.getPrograms(), expected_programs)
    
    def test_getModes(self):
        expected_modes = ['standby', 'dhw', 'dhwAndHeatingCooling']
        self.assertListEqual(self.heat.getModes(), expected_modes)
