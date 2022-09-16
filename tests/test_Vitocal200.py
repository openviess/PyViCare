import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.helper import now_is
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal200(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal200.json')
        self.device = HeatPump(self.service)

    def test_getCompressorActive(self):
        self.assertEqual(self.device.compressors[0].getActive(), False)

    def test_getCompressorHours(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHours(), 11362.7)

    def test_getAvailableCompressors(self):
        self.assertEqual(self.device.getAvailableCompressors(), ['0'])

    def test_getCompressorStarts(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getStarts(), 5101)

    def test_getCompressorHoursLoadClass1(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass1(), 283)

    def test_getCompressorHoursLoadClass2(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass2(), 4336)

    def test_getCompressorHoursLoadClass3(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass3(), 5275)

    def test_getCompressorHoursLoadClass4(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass4(), 611)

    def test_getCompressorHoursLoadClass5(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass5(), 606)

    def test_getHeatingCurveSlope(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveSlope(), 0.3)

    def test_getHeatingCurveShift(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveShift(), -5)

    def test_getReturnTemperature(self):
        self.assertAlmostEqual(self.device.getReturnTemperature(), 25.6)

    def test_getReturnTemperaturePrimaryCircuit(self):
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.getReturnTemperaturePrimaryCircuit)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 13.4)

    def test_getPrograms(self):
        expected_programs = ['active', 'comfort', 'eco',
                             'fixed', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['standby', 'dhw', 'dhwAndHeatingCooling']
        self.assertListEqual(
            self.device.circuits[0].getModes(), expected_modes)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), False)

    def test_getDomesticHotWaterActiveMode_fri_10_10_time(self):
        with now_is('2021-09-10 10:10:00'):
            self.assertEqual(
                self.device.getDomesticHotWaterActiveMode(), 'temp-2')

    def test_getDomesticHotWaterDesiredTemperature_fri_10_10_time(self):
        with now_is('2021-09-10 10:10:00'):
            self.assertEqual(
                self.device.getDomesticHotWaterDesiredTemperature(), 60)

    def test_getDomesticHotWaterDesiredTemperature_fri_20_00_time(self):
        with now_is('2021-09-10 20:00:00'):
            self.assertEqual(
                self.device.getDomesticHotWaterDesiredTemperature(), 50)
