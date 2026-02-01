import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal300G(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal300G_CU401B.json')
        self.device = HeatPump(self.service)

    def test_compressor_getActive(self):
        self.assertEqual(self.device.compressors[0].getActive(), True)

    def test_compressor_getHours(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHours(), 942.4)

    def test_compressor_getStarts(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getStarts(), 363)

    # Load class tests require fallback logic from PR #689
    # Data is in statistics.load instead of statistics
    @unittest.skip("Requires PR #689 for statistics.load fallback")
    def test_compressor_getHoursLoadClass1(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass1(), 5)

    @unittest.skip("Requires PR #689 for statistics.load fallback")
    def test_compressor_getHoursLoadClass2(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass2(), 233)

    @unittest.skip("Requires PR #689 for statistics.load fallback")
    def test_compressor_getHoursLoadClass3(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass3(), 448)

    @unittest.skip("Requires PR #689 for statistics.load fallback")
    def test_compressor_getHoursLoadClass4(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass4(), 249)

    @unittest.skip("Requires PR #689 for statistics.load fallback")
    def test_compressor_getHoursLoadClass5(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass5(), 3)

    # This device only has circuit "1" enabled (circuits[0] in the list)
    def test_getHeatingCurveSlope(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveSlope(), 1.0)

    def test_getHeatingCurveShift(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveShift(), 2)

    def test_getReturnTemperature(self):
        self.assertAlmostEqual(self.device.getReturnTemperature(), 35.8)

    def test_getReturnTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(self.device.getReturnTemperaturePrimaryCircuit(), 4.9)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 8.7)

    def test_getPrograms(self):
        expected_programs = ['comfort', 'eco', 'fixed', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['dhw', 'dhwAndHeating', 'forcedNormal', 'forcedReduced', 'normalStandby', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getModes(), expected_modes)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), False)
