import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal200S(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal200S.json')
        self.device = HeatPump(self.service)

    def test_getDomesticHotWaterConfiguredTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterConfiguredTemperature(), 40)

    def test_getAvailableCompressors(self):
        self.assertEqual(self.device.getAvailableCompressors(), ['0'])

    def test_getDomesticHotWaterConfiguredTemperature2(self):
        self.assertEqual(
            self.device.getDomesticHotWaterConfiguredTemperature2(), 60)

    def test_getReturnTemperature(self):
        self.assertEqual(
            self.device.getReturnTemperature(), 27.9)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 14.5)

    def test_getReturnTemperatureSecondaryCircuit(self):
        self.assertEqual(
            self.device.getReturnTemperatureSecondaryCircuit(), 27.9)
