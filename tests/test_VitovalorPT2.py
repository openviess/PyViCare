import unittest

from PyViCare.PyViCareFuelCell import FuelCell
from tests.ViCareServiceMock import ViCareServiceMock


class VitovalorPT2(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/VitovalorPT2.json')
        self.device = FuelCell(self.service)

    def test_getDomesticHotWaterConfiguredTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterConfiguredTemperature(), 47)

    def test_getReturnTemperature(self):
        self.assertEqual(
            self.device.getReturnTemperature(), 46.1)

    def test_getActive(self):
        self.assertEqual(self.device.burners[0].getActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.burners[0].getStarts(), 6218)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.burners[0].getHours(), 1688)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.burners[0].getModulation(), 0)

    def test_getVolumetricFlowReturn(self):
        self.assertEqual(self.device.getVolumetricFlowReturn(), 412)

    def test_getDomesticHotWaterMaxTemperatureLevel(self):
        self.assertEqual(self.device.getDomesticHotWaterMaxTemperatureLevel(), 10)

    def test_getDomesticHotWaterMinTemperatureLevel(self):
        self.assertEqual(self.device.getDomesticHotWaterMinTemperatureLevel(), 10)

    def test_getHydraulicSeparatorTemperature(self):
        self.assertEqual(self.device.getHydraulicSeparatorTemperature(), 46.8)

    def test_getPowerConsumptionDays(self):
        expected_consumption = [0.6, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3]
        self.assertListEqual(self.device.getPowerConsumptionDays(), expected_consumption)

    def test_getPowerConsumptionHeatingDays(self):
        expected_consumption = [0.6, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3]
        self.assertListEqual(self.device.getPowerConsumptionHeatingDays(), expected_consumption)

    def test_getGasConsumptionTotalDays(self):
        expected_consumption = [2, 4.1, 4.1, 4.1, 4.1, 4.199999999999999, 4.1, 4.199999999999999]
        self.assertListEqual(self.device.getGasConsumptionTotalDays(), expected_consumption)
