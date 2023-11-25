import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens300W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitodens300W.json')
        self.device = GazBoiler(self.service)

    def test_getActive(self):
        self.assertEqual(self.device.burners[0].getActive(), False)

    def test_getDomesticHotWaterChargingLevel(self):
        self.assertEqual(self.device.getDomesticHotWaterChargingLevel(), 0)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.burners[0].getStarts(), 14315)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.burners[0].getHours(), 18726.3)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.burners[0].getModulation(), 0)

    def test_getPrograms(self):
        expected_programs = ['comfort', 'eco', 'external', 'holiday', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['standby', 'dhw', 'dhwAndHeating', 'forcedReduced', 'forcedNormal']
        self.assertListEqual(
            self.device.circuits[0].getModes(), expected_modes)

    def test_getPowerConsumptionDays(self):
        expected_consumption = [0.219, 0.316, 0.32, 0.325, 0.311, 0.317, 0.312, 0.313]
        self.assertEqual(self.device.getPowerConsumptionDays(),
                         expected_consumption)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), True)

    def test_getCurrentDesiredTemperature(self):
        self.assertEqual(
            self.device.circuits[0].getCurrentDesiredTemperature(), None)

    # Is currently (August, 2021) not supported by the Viessman API even though it works for the Vitodens 200W.
    def test_getDomesticHotWaterOutletTemperature(self):
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.getDomesticHotWaterOutletTemperature)

    def test_getDomesticHotWaterCirculationScheduleModes(self):
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.getDomesticHotWaterCirculationScheduleModes)
