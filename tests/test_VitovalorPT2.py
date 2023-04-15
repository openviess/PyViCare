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

    def test_getFuelCellOperatingModeActive(self):
        self.assertEqual(self.device.getFuelCellOperatingModeActive(), "economical")

    def test_getFuelCellPowerProductionUnit(self):
        # Returns the unit for the fuel cell's power production statistics, e.g. kilowattHour
        self.assertEqual(self.device.getFuelCellPowerProductionUnit(), "kilowattHour")

    def test_getFuelCellPowerProductionDays(self):
        self.assertEqual(self.device.getFuelCellPowerProductionDays(), [0.8, 18.3, 13, 15.1, 16.5, 18.3, 8.6, 18.3])

    def test_getFuelCellPowerProductionToday(self):
        self.assertEqual(self.device.getFuelCellPowerProductionToday(), 0.8)

    def test_getFuelCellPowerProductionWeeks(self):
        self.assertEqual(self.device.getFuelCellPowerProductionWeeks(), [63.7, 95.80000000000001, 60.9, 40.2, 41.300000000000004, 40.6, 58.699999999999996])

    def test_getFuelCellPowerProductionThisWeek(self):
        self.assertEqual(self.device.getFuelCellPowerProductionThisWeek(), 63.7)

    def test_getFuelCellPowerProductionMonths(self):
        self.assertEqual(self.device.getFuelCellPowerProductionMonths(), [212.6, 206.7, 190, 130.4, 39.9, 0, 187.4, 327.2, 411.3, 441.2, 500.7, 460.5, 431.4])

    def test_getFuelCellPowerProductionThisMonth(self):
        self.assertEqual(self.device.getFuelCellPowerProductionThisMonth(), 212.6)

    def test_getFuelCellPowerProductionYears(self):
        self.assertEqual(self.device.getFuelCellPowerProductionYears(), [2647.4, 1609.2])

    def test_getFuelCellPowerProductionThisYear(self):
        self.assertEqual(self.device.getFuelCellPowerProductionThisYear(), 2647.4)

    def test_getFuelCellOperatingPhase(self):
        self.assertEqual(self.device.getFuelCellOperatingPhase(), "standby")

    def test_getFuelCellPowerProductionCurrentUnit(self):
        self.assertEqual(self.device.getFuelCellPowerProductionCurrentUnit(), "watt")

    def test_getFuelCellPowerProductionCurrent(self):
        self.assertEqual(self.device.getFuelCellPowerProductionCurrent(), 0)

    def test_getFuelCellPowerPurchaseCurrentUnit(self):
        self.assertEqual(self.device.getFuelCellPowerPurchaseCurrentUnit(), "watt")

    def test_getFuelCellPowerPurchaseCurrent(self):
        self.assertEqual(self.device.getFuelCellPowerPurchaseCurrent(), 594)

    def test_getFuelCellPowerSoldCurrentUnit(self):
        self.assertEqual(self.device.getFuelCellPowerSoldCurrentUnit(), "watt")

    def test_getFuelCellPowerSoldCurrent(self):
        self.assertEqual(self.device.getFuelCellPowerSoldCurrent(), 0)

    def test_getFuelCellPowerProductionCumulativeUnit(self):
        self.assertEqual(self.device.getFuelCellPowerProductionCumulativeUnit(), "kilowattHour")

    def test_getFuelCellPowerProductionCumulative(self):
        self.assertEqual(self.device.getFuelCellPowerProductionCumulative(), 4537)

    def test_getFuelCellPowerPurchaseCumulativeUnit(self):
        self.assertEqual(self.device.getFuelCellPowerPurchaseCumulativeUnit(), "kilowattHour")

    def test_getFuelCellPowerPurchaseCumulative(self):
        self.assertEqual(self.device.getFuelCellPowerPurchaseCumulative(), 3767.1)

    def test_getFuelCellPowerSoldCumulativeUnit(self):
        self.assertEqual(self.device.getFuelCellPowerSoldCumulativeUnit(), "kilowattHour")

    def test_getFuelCellPowerSoldCumulative(self):
        self.assertEqual(self.device.getFuelCellPowerSoldCumulative(), 1822.1)

    def test_getFuelCellFlowReturnTemperatureUnit(self):
        self.assertEqual(self.device.getFuelCellFlowReturnTemperatureUnit(), "celsius")

    def test_getFuelCellFlowReturnTemperature(self):
        self.assertEqual(self.device.getFuelCellFlowReturnTemperature(), 33.9)

    def test_getFuelCellFlowSupplyTemperatureUnit(self):
        self.assertEqual(self.device.getFuelCellFlowSupplyTemperatureUnit(), "celsius")

    def test_getFuelCellFlowSupplyTemperature(self):
        self.assertEqual(self.device.getFuelCellFlowSupplyTemperature(), 39)

    def test_getFuelCellOperationHours(self):
        self.assertEqual(self.device.getFuelCellOperationHours(), 11594)

    def test_getFuelCellProductionHours(self):
        self.assertEqual(self.device.getFuelCellProductionHours(), 5980)

    def test_getFuelCellProductionStarts(self):
        self.assertEqual(self.device.getFuelCellProductionStarts(), 383)

    def test_getFuelCellGasConsumptionUnit(self):
        self.assertEqual(self.device.getFuelCellGasConsumptionUnit(), "cubicMeter")

    def test_getFuelCellGasConsumptionDays(self):
        self.assertEqual(self.device.getFuelCellGasConsumptionDays(), [1.5, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2])

    def test_getFuelCellGasConsumptionToday(self):
        self.assertEqual(self.device.getFuelCellGasConsumptionToday(), 1.5)

    def test_getFuelCellGasConsumptionWeeks(self):
        self.assertEqual(self.device.getFuelCellGasConsumptionWeeks(), [2.3000000000000003, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4])

    def test_getFuelCellGasConsumptionThisWeek(self):
        self.assertEqual(self.device.getFuelCellGasConsumptionThisWeek(), 2.3000000000000003)

    def test_getFuelCellGasConsumptionMonths(self):
        self.assertEqual(self.device.getFuelCellGasConsumptionMonths(), [4.9, 55.5, 50.9, 35.1, 10.9, 0, 49.4, 85.4, 108.5, 118, 132.5, 120.7, 111.5])

    def test_getFuelCellGasConsumptionThisMonth(self):
        self.assertEqual(self.device.getFuelCellGasConsumptionThisMonth(), 4.9)

    def test_getFuelCellGasConsumptionYears(self):
        self.assertEqual(self.device.getFuelCellGasConsumptionYears(), [651.1, 416.6])

    def test_getFuelCellGasConsumptionThisYear(self):
        self.assertEqual(self.device.getFuelCellGasConsumptionThisYear(), 651.1)
