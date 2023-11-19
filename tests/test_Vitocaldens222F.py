import unittest

from PyViCare.PyViCareHybrid import Hybrid
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocaldens222F(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocaldens222F.json')
        self.device = Hybrid(self.service)

    def test_getAvailableCircuits(self):
        self.assertEqual(self.device.getAvailableCircuits(), ['1'])

    def test_getAvailableBurners(self):
        self.assertEqual(self.device.getAvailableBurners(), ['0'])

    def test_getAvailableCompressors(self):
        self.assertEqual(self.device.getAvailableCompressors(), ['0'])

    def test_getActive(self):
        self.assertEqual(self.device.burners[0].getActive(), False)

    def test_getBufferTopTemperature(self):
        self.assertEqual(
            self.device.getBufferTopTemperature(), 36)

    def test_getBufferMainTemperature(self):
        self.assertEqual(
            self.device.getBufferMainTemperature(), 36)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.getBurner(0).getStarts(), 1306)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.getBurner(0).getHours(), 1639)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.getBurner(0).getModulation(), 0)

    def test_getCompressorHours(self):
        self.assertEqual(self.device.getCompressor(0).getHours(), 1.4)

    def test_getPrograms(self):
        expected_programs = ['comfort', 'eco', 'fixed', 'normal', 'reduced', 'standby']
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

    def test_getHotWaterStorageTemperatureTop(self):
        self.assertEqual(
            self.device.getHotWaterStorageTemperatureTop(), 50.9)
