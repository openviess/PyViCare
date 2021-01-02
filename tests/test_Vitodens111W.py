import unittest
from tests.ViCareServiceForTesting import ViCareServiceForTesting
from PyViCare.PyViCareGazBoiler import GazBoiler

class Vitodens111W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceForTesting('response_Vitodens111W.json', 0)
        self.gaz = GazBoiler(None, None, None, 0, 0, self.service)

    def test_getBurnerActive(self):
        self.assertEqual(self.gaz.getBurnerActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.gaz.getBurnerStarts(), 12648)

    def test_getPowerConsumptionDays_fails(self):
        self.assertEqual(self.gaz.getPowerConsumptionDays(), 'error')

    def test_getMonthSinceLastService_fails(self):
        self.assertEqual(self.gaz.getMonthSinceLastService(), "KeyError: 'properties'")
