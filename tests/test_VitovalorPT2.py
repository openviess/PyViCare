import unittest

from PyViCare.PyViCareFuelCell import FuelCell
from tests.ViCareServiceMock import ViCareServiceMock


class VitovalorPT2(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/VitovalorPT2.json')
        self.device = FuelCell(self.service)

    def test_getDomesticHotWaterConfiguredTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterConfiguredTemperature(), 45)

    def test_getReturnTemperature(self):
        self.assertEqual(
            self.device.getReturnTemperature(), 22.2)

    def test_getActive(self):
        self.assertEqual(self.device.burners[0].getActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.burners[0].getStarts(), 3862)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.burners[0].getHours(), 282)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.burners[0].getModulation(), 0)

    def test_getVolumetricFlowReturn(self):
        self.assertEqual(self.device.getVolumetricFlowReturn(), 513)

    def test_getDomesticHotWaterMaxTemperatureLevel(self):
        self.assertEqual(self.device.getDomesticHotWaterMaxTemperatureLevel(), 10)

    def test_getDomesticHotWaterMinTemperatureLevel(self):
        self.assertEqual(self.device.getDomesticHotWaterMinTemperatureLevel(), 10)

    def test_getHydraulicSeparatorTemperature(self):
        self.assertEqual(self.device.getHydraulicSeparatorTemperature(), 22.3)

    def test_getPowerConsumptionDays(self):
        expected_consumption = [0.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]
        self.assertListEqual(self.device.getPowerConsumptionDays(), expected_consumption)

    def test_getPowerConsumptionHeatingDays(self):
        expected_consumption = [0.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]
        self.assertListEqual(self.device.getPowerConsumptionHeatingDays(), expected_consumption)

    def test_getGasConsumptionTotalDays(self):
        expected_consumption = [1.5, 0.2, 0.30000000000000004, 0.2, 0.4, 0.6000000000000001, 1.7, 0.2]
        self.assertListEqual(self.device.getGasConsumptionTotalDays(), expected_consumption)
