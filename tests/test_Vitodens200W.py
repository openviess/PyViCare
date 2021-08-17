import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens200W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitodens200W.json')
        self.device = GazBoiler(self.service)

    def test_getBurnerActive(self):
        self.assertEqual(self.device.getBurnerActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.circuits[0].getBurnerStarts(), 8125)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.circuits[0].getBurnerHours(), 5605)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.circuits[0].getBurnerModulation(), 0)

    def test_getPrograms(self):
        expected_programs = [
            'active', 'comfort', 'forcedLastFromSchedule', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['standby', 'heating', 'dhw', 'dhwAndHeating']
        self.assertListEqual(
            self.device.circuits[0].getModes(), expected_modes)

    # Is currently (August, 2021) not supported by the Viessman API
    def test_getPowerConsumptionDays(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.getPowerConsumptionDays)

    def test_getDomesticHotWaterMaxTemperature(self):
        self.assertEqual(self.device.getDomesticHotWaterMaxTemperature(), 60)

    def test_getDomesticHotWaterMinTemperature(self):
        self.assertEqual(self.device.getDomesticHotWaterMinTemperature(), 10)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), False)

    def test_getDomesticHotWaterOutletTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterOutletTemperature(), 41.9)

    def test_getDomesticHotWaterConfiguredTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterConfiguredTemperature(), 55)

    def test_getDomesticHotWaterCirculationScheduleModes(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationScheduleModes(), ['on'])
