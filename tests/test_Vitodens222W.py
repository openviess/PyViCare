import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens222W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitodens222W.json')
        self.device = GazBoiler(self.service)

    def test_getBurnerActive(self):
        self.assertEqual(self.device.getBurnerActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.burners[0].getStarts(), 79167)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.burners[0].getHours(), 25123.2)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.burners[0].getModulation(), 0)

    def test_getPrograms(self):
        expected_programs = ['active', 'comfort', 'eco',
                             'external', 'holiday', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['standby', 'dhw', 'dhwAndHeating',
                          'forcedReduced', 'forcedNormal']
        self.assertListEqual(
            self.device.circuits[0].getModes(), expected_modes)

    def test_getPowerConsumptionDays(self):
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.getPowerConsumptionDays)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), False)

    def test_getDomesticHotWaterOutletTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterOutletTemperature(), 44.8)

    def test_getDomesticHotWaterCirculationScheduleModes(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationScheduleModes(), ['on'])

    def test_getOutsideTemperature(self):
        self.assertEqual(
            self.device.getOutsideTemperature(), 16.3)

    def test_getBoilerTemperature(self):
        self.assertEqual(
            self.device.getBoilerTemperature(), 73)
