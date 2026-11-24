import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal250ANoiseReduction(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/Vitocal250A_NoiseReduction.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_getNoiseReductionLevels(self):
        self.assertEqual(self.device.getNoiseReductionLevels(), ["notReduced", "slightlyReduced", "maxReduced"])

    def test_getNoiseReductionLevel(self):
        self.assertEqual(self.device.getNoiseReductionLevel(), "maxReduced")

    def test_getDomesticHotWaterScheduleConstraints(self):
        self.assertEqual(self.device.getDomesticHotWaterScheduleModes(), ['on'])
        self.assertEqual(self.device.getDomesticHotWaterScheduleMaxEntries(), 4)
        self.assertIs(self.device.getDomesticHotWaterScheduleOverlapAllowed(), False)
        self.assertEqual(self.device.getDomesticHotWaterScheduleResolution(), 10)

    def test_getHeatingScheduleConstraints(self):
        self.assertEqual([circuit.circuit for circuit in self.device.circuits], ['1', '2'])
        for circuit in self.device.circuits:
            self.assertEqual(circuit.getHeatingScheduleModes(), ['normal', 'comfort'])
            self.assertEqual(circuit.getHeatingScheduleMaxEntries(), 4)
            self.assertIs(circuit.getHeatingScheduleOverlapAllowed(), False)
            self.assertEqual(circuit.getHeatingScheduleResolution(), 10)
