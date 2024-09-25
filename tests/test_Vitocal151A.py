import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.helper import now_is
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal200(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal151A.json')
        self.device = HeatPump(self.service)

    def test_getPowerConsumptionCooling(self):
        self.assertEqual(self.device.getPowerConsumptionCoolingUnit(), "kilowattHour")
        self.assertEqual(self.device.getPowerConsumptionCoolingCurrentDay(), 0)
        self.assertEqual(self.device.getPowerConsumptionCoolingCurrentMonth(), 0.1)
        self.assertEqual(self.device.getPowerConsumptionCoolingCurrentYear(), 0.1)
