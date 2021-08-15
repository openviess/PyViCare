import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens300W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitodens300W.json')
        self.device = GazBoiler(self.service)

    def test_getBurnerActive(self):
        self.assertEqual(self.device.getBurnerActive(), True)

    # Is currently (August, 2021) not supported by the Viessman API even though it works for the Vitodens 200W.
    def test_getBurnerStarts(self):
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.circuits[0].getBurnerStarts)

    # Is currently (August, 2021) not supported by the Viessman API even though it works for the Vitodens 200W.
    def test_getBurnerHours(self):
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.circuits[0].getBurnerHours)

    # Is currently (August, 2021) not supported by the Viessman API even though it works for the Vitodens 200W.
    def test_getBurnerModulation(self):
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.circuits[0].getBurnerModulation)

    def test_getPrograms(self):
        expected_programs = ['active', 'comfort', 'eco',
                             'external', 'holiday', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['dhw', 'dhwAndHeating',
                          'forcedNormal', 'forcedReduced', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getModes(), expected_modes)

    def test_getPowerConsumptionDays(self):
        expected_consumption = [0.103, 0.186, 0.224,
                                0.254, 0.202, 0.207, 0.185, 0.145]
        self.assertEqual(self.device.getPowerConsumptionDays(),
                         expected_consumption)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), False)

    # Is currently (August, 2021) not supported by the Viessman API even though it works for the Vitodens 200W.
    def test_getDomesticHotWaterOutletTemperature(self):
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.getDomesticHotWaterOutletTemperature)

    def test_getDomesticHotWaterCirculationScheduleModes(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationScheduleModes(), ['on'])
