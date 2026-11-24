import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens100WB1HC26(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/Vitodens100W_B1HC-26.json')
        self.device = GazBoiler(self.accessor, self.service)

    def test_getDomesticHotWaterScheduleConstraints(self):
        self.assertEqual(self.device.getDomesticHotWaterScheduleModes(), ['on'])
        self.assertEqual(self.device.getDomesticHotWaterScheduleMaxEntries(), 20)
        self.assertIs(self.device.getDomesticHotWaterScheduleOverlapAllowed(), True)
        self.assertEqual(self.device.getDomesticHotWaterScheduleResolution(), 5)

    def test_getHeatingScheduleConstraints(self):
        circuit = self.device.circuits[0]
        self.assertEqual(circuit.getHeatingScheduleModes(), ['comfort', 'normal'])
        self.assertEqual(circuit.getHeatingScheduleMaxEntries(), 20)
        self.assertIs(circuit.getHeatingScheduleOverlapAllowed(), True)
        self.assertEqual(circuit.getHeatingScheduleResolution(), 5)
