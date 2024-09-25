import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens222W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitodens222W.json')
        self.device = GazBoiler(self.service)

    def test_getActive(self):
        self.assertEqual(self.device.burners[0].getActive(), True)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.burners[0].getStarts(), 8299)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.burners[0].getHours(), 5674)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.burners[0].getModulation(), 15.8)

    def test_getPrograms(self):
        expected_programs = ['comfort', 'forcedLastFromSchedule', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['standby', 'heating', 'dhw', 'dhwAndHeating']
        self.assertListEqual(
            self.device.circuits[0].getModes(), expected_modes)

    def test_getPowerConsumptionDays(self):
        expected_consumption = [0.4, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        self.assertListEqual(self.device.getPowerConsumptionDays(), expected_consumption)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), False)

    def test_getDomesticHotWaterOutletTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterOutletTemperature(), 39.8)

    def test_getDomesticHotWaterCirculationScheduleModes(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationScheduleModes(), ['on'])

    def test_getOutsideTemperature(self):
        self.assertEqual(
            self.device.getOutsideTemperature(), 11.9)

    def test_getOneTimeCharge(self):
        self.assertEqual(
            self.device.getOneTimeCharge(), False)

    def test_getBoilerTemperature(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.getBoilerTemperature)
