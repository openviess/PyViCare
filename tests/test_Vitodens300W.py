import unittest
from tests.ViCareServiceMock import ViCareServiceMock
from PyViCare.PyViCareGazBoiler import GazBoiler
import PyViCare.Feature

class Vitodens300W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response_Vitodens300W.json')
        self.device = GazBoiler(self.service)
        PyViCare.Feature.raise_exception_on_not_supported_device_feature = True

    def test_getBurnerActive(self):
        self.assertEqual(self.device.getBurnerActive(), True)

#    def test_getBurnerStarts(self):
#        self.assertEqual(self.device.circuits[0].getBurnerStarts(), 8028)

#    def test_getBurnerHours(self):
#        self.assertEqual(self.device.circuits[0].getBurnerHours(), 5570)

#    def test_getBurnerModulation(self):
#        self.assertEqual(self.device.circuits[0].getBurnerModulation(), 11.1)

    def test_getPrograms(self):
        expected_programs = ['active', 'comfort', 'eco', 'external', 'holiday', 'normal', 'reduced', 'standby']
        self.assertListEqual(self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes =  ['dhw', 'dhwAndHeating', 'forcedNormal', 'forcedReduced', 'standby']
        self.assertListEqual(self.device.circuits[0].getModes(), expected_modes)

    def test_getPowerConsumptionDays(self):
        expected_consumption = [0.103, 0.186, 0.224, 0.254, 0.202, 0.207, 0.185, 0.145]
        self.assertEqual(self.device.getPowerConsumptionDays(), expected_consumption)

    def test_getFrostProtectionActive(self):
        self.assertEqual(self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(self.device.getDomesticHotWaterCirculationPumpActive(), False)

#    def test_getDomesticHotWaterOutletTemperature(self):
#        self.assertEqual(self.device.getDomesticHotWaterOutletTemperature(), 58)

    def test_getDomesticHotWaterCirculationSchedule(self):
        self.assertEqual(self.device.getDomesticHotWaterCirculationSchedule(), ['on'])

        
