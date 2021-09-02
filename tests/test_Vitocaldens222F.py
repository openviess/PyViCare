import unittest

from PyViCare.PyViCareHybrid import Hybrid
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocaldens222F(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocaldens222F.json')
        self.device = Hybrid(self.service)

    def test_getAvailableCircuits(self):
        self.assertEqual(self.device.getAvailableCircuits(), ['1'])

    def test_getBurnerActive(self):
        self.assertEqual(self.device.getBurnerActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.getCircuit(0).getBurnerStarts(), 1306)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.getCircuit(0).getBurnerHours(), 1639)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.getCircuit(0).getBurnerModulation(), 0)
    
    def test_getCompressorHours(self):
        self.assertEqual(self.device.getCircuit(0).getCompressorHours(), 1.4)

    def test_getPrograms(self):
        expected_programs = ['active', 'comfort', 'eco', 'fixed',
                             'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.getCircuit(1).getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['standby', 'dhw', 'dhwAndHeating']
        self.assertListEqual(
            self.device.getCircuit(1).getModes(), expected_modes)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.getCircuit(1).getFrostProtectionActive(), False)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), False)

    def test_getDomesticHotWaterOutletTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterOutletTemperature(), 41.7)

    def test_getDomesticHotWaterCirculationScheduleModes(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationScheduleModes(), ['5/25-cycles', '5/10-cycles', 'on'])

    def test_getOutsideTemperature(self):
        self.assertEqual(
            self.device.getOutsideTemperature(), 15.3)