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
        self.assertEqual(self.device.getCompressor(0).getActive(), False)

    def test_getCompressorHours(self):
        self.assertAlmostEqual(
            self.device.getCompressor(0).getHours(), 13651.9)

    def test_getAvailableCompressors(self):
        self.assertEqual(self.device.getAvailableCompressors(), ['0'])

    def test_getCompressorStarts(self):
        self.assertAlmostEqual(
            self.device.getCompressor(0).getStarts(), 6973)

    def test_getCompressorHoursLoadClass1(self):
        self.assertAlmostEqual(
            self.device.getCompressor(0).getHoursLoadClass1(), 366)

    def test_getCompressorHoursLoadClass2(self):
        self.assertAlmostEqual(
            self.device.getCompressor(0).getHoursLoadClass2(), 5579)

    def test_getCompressorHoursLoadClass3(self):
        self.assertAlmostEqual(
            self.device.getCompressor(0).getHoursLoadClass3(), 6024)

    def test_getCompressorHoursLoadClass4(self):
        self.assertAlmostEqual(
            self.device.getCompressor(0).getHoursLoadClass4(), 659)

    def test_getCompressorHoursLoadClass5(self):
        self.assertAlmostEqual(
            self.device.getCompressor(0).getHoursLoadClass5(), 715)

    def test_getCompressorPhase(self):
        self.assertEqual(
            self.device.getCompressor(0).getPhase(), "off")

    def test_getHeatingCurveSlope(self):
        self.assertAlmostEqual(
            self.device.getCircuit(0).getHeatingCurveSlope(), 0.4)

    def test_getHeatingCurveShift(self):
        self.assertAlmostEqual(
            self.device.getCircuit(0).getHeatingCurveShift(), -6)

    def test_getReturnTemperature(self):
        self.assertAlmostEqual(self.device.getReturnTemperature(), 22.7)

    def test_getReturnTemperaturePrimaryCircuit(self):
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.getReturnTemperaturePrimaryCircuit)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 11.6)

    def test_getPrograms(self):
        expected_programs = ['comfort', 'eco', 'fixed', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.getCircuit(0).getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['dhw', 'dhwAndHeatingCooling', 'standby']
        self.assertListEqual(
            self.device.getCircuit(0).getModes(), expected_modes)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), False)

    def test_getDomesticHotWaterActiveMode_fri_10_10_time(self):
        with now_is('2021-09-10 10:10:00'):
            self.assertIsNone(self.device.getDomesticHotWaterActiveMode())

    def test_getDomesticHotWaterDesiredTemperature_fri_10_10_time(self):
        with now_is('2021-09-10 10:10:00'):
            self.assertIsNone(
                self.device.getDomesticHotWaterDesiredTemperature())

    def test_getDomesticHotWaterDesiredTemperature_fri_20_00_time(self):
        with now_is('2021-09-10 20:00:00'):
            self.assertEqual(
                self.device.getDomesticHotWaterDesiredTemperature(), 50)

    def test_getActiveProgramMinTemperature(self):
        self.assertEqual(self.device.getCircuit(0).getActiveProgramMinTemperature(), 10)

    def test_getActiveProgramMaxTemperature(self):
        self.assertEqual(self.device.getCircuit(0).getActiveProgramMaxTemperature(), 30)

    def test_getActiveProgramMaxTemperature(self):
        self.assertEqual(self.device.getCircuit(0).getActiveProgramStepping(), 1)

    def test_getNormalProgramMinTemperature(self):
        self.assertEqual(self.device.getCircuit(0).getProgramMinTemperature("normal"), 10)

    def test_getNormalProgramMaxTemperature(self):
        self.assertEqual(self.device.getCircuit(0).getProgramMaxTemperature("normal"), 30)
        
    def test_getNormalProgramStepping(self):
        self.assertEqual(self.device.getCircuit(0).getProgramStepping("normal"), 1)
