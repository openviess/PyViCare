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
