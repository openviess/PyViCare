import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal300G(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal300G.json')
        self.device = HeatPump(self.service)

    def test_getCompressorActive(self):
        self.assertEqual(self.device.compressors[0].getActive(), False)

    def test_getCompressorHours(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHours(), 1762.41)

    def test_getCompressorStarts(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getStarts(), 3012)

    def test_getCompressorHoursLoadClass1(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass1(), 30)

    def test_getCompressorHoursLoadClass2(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass2(), 703)

    def test_getCompressorHoursLoadClass3(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass3(), 878)

    def test_getCompressorHoursLoadClass4(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass4(), 117)

    def test_getCompressorHoursLoadClass5(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass5(), 20)

    def test_getHeatingCurveSlope(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveSlope(), 0.8)

    def test_getHeatingCurveShift(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveShift(), -5)

    def test_getReturnTemperature(self):
        self.assertAlmostEqual(self.device.getReturnTemperature(), 18.9)

    def test_getReturnTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(self.device.getReturnTemperaturePrimaryCircuit(), 18.4)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 18.2)

    def test_getPrograms(self):
        expected_programs = ['comfort', 'eco', 'fixed', 'holiday', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['dhw', 'dhwAndHeating', 'forcedNormal', 'forcedReduced', 'standby', 'normalStandby']
        self.assertListEqual(
            self.device.circuits[0].getModes(), expected_modes)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), False)
