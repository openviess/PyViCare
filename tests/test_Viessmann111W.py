import unittest
from tests.ViCareServiceForTesting import ViCareServiceForTesting
from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareGazBoiler import GazBoiler

class Viessmann111W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceForTesting('response_Viessman_111W.json', 0)
        self.gaz = GazBoiler(None, None, None, 0, 0, self.service)

    def test_getBurnerActive(self):
        self.assertEqual(self.gaz.getBurnerActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.gaz.getBurnerStarts(), 12648)

    def test_getPowerConsumptionDays_fails(self):
        self.assertEqual(self.gaz.getPowerConsumptionDays(), 'error')

    def test_activateComfort(self):
        self.gaz.activateComfort()
        self.assertEqual(self.service.setPropertyData[0]['action'], 'activate')
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'heating.circuits.0.operating.programs.comfort')

    def test_deactivateComfort(self):
        self.gaz.deactivateComfort()
        self.assertEqual(self.service.setPropertyData[0]['action'], 'deactivate')
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'heating.circuits.0.operating.programs.comfort')
        
if __name__ == '__main__':
    unittest.main()