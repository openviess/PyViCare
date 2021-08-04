import unittest
from tests.ViCareServiceMock import ViCareServiceMock
from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError


class Vitodens333F(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitodens333F.json')
        self.device = GazBoiler(self.service)

    def test_getBurnerActive(self):
        self.assertEqual(self.device.getBurnerActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.circuits[0].getBurnerStarts(), 13987)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.circuits[0].getBurnerHours(), 14071.8)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.circuits[0].getBurnerModulation(), 0)

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
        expected_consumption = [0.097, 0.162, 0.166,
                                0.162, 0.159, 0.173, 0.182, 0.159]
        self.assertEqual(self.device.getPowerConsumptionDays(),
                         expected_consumption)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), False)

    def test_getDomesticHotWaterOutletTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterOutletTemperature(), 29.8)

    def test_getDomesticHotWaterCirculationScheduleModes(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationScheduleModes(), ['on'])

    def test_getOutsideTemperature(self):
        self.assertEqual(
            self.device.getOutsideTemperature(), 26.2)

    def test_getBoilerTemperature(self):
        self.assertEqual(
            self.device.getBoilerTemperature(), 35)
