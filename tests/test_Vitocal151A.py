import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal200(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "[device]")
        self.service = ViCareServiceMock('response/Vitocal151A.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_getPowerConsumptionCooling(self):
        self.assertEqual(self.device.getPowerConsumptionCoolingUnit(), "kilowattHour")
        self.assertEqual(self.device.getPowerConsumptionCoolingToday(), 0)
        self.assertEqual(self.device.getPowerConsumptionCoolingThisMonth(), 0.1)
        self.assertEqual(self.device.getPowerConsumptionCoolingThisYear(), 0.1)
