import unittest
from tests.ViCareServiceForTesting import ViCareServiceForTesting
from PyViCare.PyViCareGazBoiler import GazBoiler

class Vitodens222F(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceForTesting('response_Vitodens222F.json', 0)
        self.gaz = GazBoiler(None, None, None, 0, 0, self.service)

    def test_getBurnerActive(self):
        self.assertEqual(self.gaz.getBurnerActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.gaz.getBurnerStarts(), 5898)

    def test_getPowerConsumptionToday(self):
        self.assertEqual(self.gaz.getPowerConsumptionToday(), 1)

    def test_getMonthSinceLastService_fails(self):
        self.assertEqual(self.gaz.getMonthSinceLastService(), "KeyError: 'properties'")

    def test_getSupplyTemperature(self):
        self.assertAlmostEqual(self.gaz.getSupplyTemperature(), 41.9)

    def test_getPrograms(self):
        expected_programs = ['active',
                            'comfort',
                            'forcedLastFromSchedule',
                            'holiday',
                            'holidayAtHome',
                            'normal',
                            'reduced',
                            'standby']
        self.assertListEqual(self.gaz.getPrograms(), expected_programs)
