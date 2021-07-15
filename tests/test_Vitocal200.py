import unittest
from tests.ViCareServiceMock import ViCareServiceMock
from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCare import PyViCareNotSupportedFeatureError
import PyViCare.Feature

class Vitocal200(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response_Vitocal200.json', 0)
        self.device = HeatPump(None, None, None, 0, 0, self.service)
        PyViCare.Feature.raise_exception_on_not_supported_device_feature = True
        
    def test_getCompressorActive(self):
        self.assertEqual(self.device.getCompressorActive(), False)

    def test_getCompressorHours(self):
        self.assertAlmostEqual(self.device.getCompressorHours(), 8583.2)

    def test_getCompressorStarts(self):
        self.assertAlmostEqual(self.device.getCompressorStarts(), 3180)

    def test_getCompressorHoursLoadClass1(self):
        self.assertAlmostEqual(self.device.getCompressorHoursLoadClass1(), 227)

    def test_getCompressorHoursLoadClass2(self):
        self.assertAlmostEqual(self.device.getCompressorHoursLoadClass2(), 3294)

    def test_getCompressorHoursLoadClass3(self):
        self.assertAlmostEqual(self.device.getCompressorHoursLoadClass3(), 3903)

    def test_getCompressorHoursLoadClass4(self):
        self.assertAlmostEqual(self.device.getCompressorHoursLoadClass4(), 506)

    def test_getCompressorHoursLoadClass5(self):
        self.assertAlmostEqual(self.device.getCompressorHoursLoadClass5(), 461)

    def test_getHeatingCurveSlope(self):
        self.assertAlmostEqual(self.device.getHeatingCurveSlope(), 0.3)

    def test_getHeatingCurveShift(self):
        self.assertAlmostEqual(self.device.getHeatingCurveShift(), -5)

    def test_getReturnTemperature(self):
        self.assertAlmostEqual(self.device.getReturnTemperature(), 27.5)

    def test_getReturnTemperaturePrimaryCircuit(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.getReturnTemperaturePrimaryCircuit)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(self.device.getSupplyTemperaturePrimaryCircuit(), 18.9)

    def test_getPrograms(self):
        expected_programs = ['active', 'comfort', 'eco', 'fixed', 'normal', 'reduced', 'standby']
        self.assertListEqual(self.device.getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['standby', 'dhw', 'dhwAndHeatingCooling']
        self.assertListEqual(self.device.getModes(), expected_modes)
