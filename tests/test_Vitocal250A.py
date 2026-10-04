import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal250A(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/Vitocal250A.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_compressor_getActive(self):
        self.assertFalse(self.device.compressors[0].getActive())

    def test_compressor_getHours(self):
        self.assertEqual(
            self.device.compressors[0].getHours(), 8118)

    def test_compressor_getStarts(self):
        self.assertEqual(
            self.device.compressors[0].getStarts(), 1502)

    def test_compressor_getPhase(self):
        self.assertEqual(
            self.device.getCompressor(0).getPhase(), "ready")

    # def test_compressor_getHeatProduction(self):
    #     self.assertEqual(self.device.compressors[0].getHeatProductionCurrent(), 13.317)
    #     self.assertEqual(self.device.compressors[0].getHeatProductionCurrentUnit(), "watt")

    # def test_compressor_getPowerConsumptionCurrent(self):
    #     self.assertEqual(self.device.compressors[0].getPowerConsumptionCurrent(), 3.107)
    #     self.assertEqual(self.device.compressors[0].getPowerConsumptionCurrentUnit(), "kilowatt")

    def test_compressor_getPowerConsumptionThisYear(self):
        # self.assertEqual(self.device.compressors[0].getPowerConsumptionDHWThisYear(), 143.0)
        # self.assertEqual(self.device.compressors[0].getPowerConsumptionHeatingThisYear(), 55.2)
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.compressors[0].getPowerConsumptionCoolingThisYear)
        # self.assertEqual(self.device.compressors[0].getPowerConsumptionTotalThisYear(), 198.2)
        # self.assertEqual(self.device.compressors[0].getPowerConsumptionTotalUnit(), "kilowattHour")

    def test_compressor_getOilTemperature(self):
        self.assertEqual(self.device.getCompressor(0).getOilTemperature(), 41.3)

    def test_compressor_getMotorChamberTemperature(self):
        self.assertEqual(self.device.getCompressor(0).getMotorChamberTemperature(), 24.2)

    def test_getHeatingCurveSlope(self):
        self.assertEqual(
            self.device.circuits[0].getHeatingCurveSlope(), 0.6)

    def test_getHeatingCurveShift(self):
        self.assertEqual(
            self.device.circuits[0].getHeatingCurveShift(), 4)

    def test_getReturnTemperature(self):
        self.assertEqual(self.device.getReturnTemperature(), 34.2)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 13.9)

    def test_getPrograms(self):
        expected_programs = ['comfortCooling', 'comfortCoolingEnergySaving', 'comfortEnergySaving', 'comfortHeating', 'fixed', 'forcedLastFromSchedule', 'frostprotection', 'normalCooling', 'normalCoolingEnergySaving', 'normalEnergySaving', 'normalHeating', 'reducedCooling', 'reducedCoolingEnergySaving', 'reducedEnergySaving', 'reducedHeating', 'standby']
        self.assertListEqual(expected_programs, self.device.circuits[0].getPrograms())

    def test_getModes(self):
        expected_modes = ['heating', 'standby']
        self.assertListEqual(expected_modes, self.device.circuits[0].getModes())

    def test_getPowerConsumptionUnit(self):
        self.assertEqual(
            self.device.getPowerConsumptionUnit(), "kilowattHour")

    def test_getPowerConsumptionToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionToday(), 7.199999999999999)

    def test_getPowerConsumptionDomesticHotWaterToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionDomesticHotWaterToday(), 2.6)

    def test_getPowerSummaryConsumptionHeatingCurrentDay(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentDay(), 4.6)

    def test_getPowerSummaryConsumptionHeatingCurrentMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentMonth(), 32.3)

    def test_getPowerSummaryConsumptionHeatingCurrentYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentYear(), 2565.7)

    def test_getPowerSummaryConsumptionHeatingLastMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingLastMonth(), 32.1)

    def test_getPowerSummaryConsumptionHeatingLastSevenDays(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingLastSevenDays(), 39.4)

    def test_getPowerSummaryConsumptionHeatingLastYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingLastYear(), 3809.6)

    def test_getPowerSummaryConsumptionHeatingUnit(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingUnit(), "kilowattHour")

    @unittest.skip("dump is not up to date, underlying data point was rernamed")
    def test_getBufferMainTemperature(self):
        self.assertEqual(
            self.device.getBufferMainTemperature(), 31.9)

    def test_getOutsideTemperature(self):
        self.assertEqual(
            self.device.getOutsideTemperature(), 12.2)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getPowerSummaryConsumptionDomesticHotWaterUnit(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterUnit(), "kilowattHour")

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentDay(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentDay(), 2.6)

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(), 16)

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentYear(), 875.0999999999999)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastMonth(), 89.7)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(), 24.5)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastYear(), 1536.8)

    def test_getDomesticHotWaterHysteresis(self):
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisUnit(), 'kelvin')
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresis(), 5)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisMin(), 1)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisMax(), 10)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisStepping(), 0.5)

    def test_getDomesticHotWaterHysteresisSwitchOn(self):
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOn(), 5)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOnMin(), 1)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOnMax(), 10)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOnStepping(), 0.5)

    def test_getDomesticHotWaterHysteresisSwitchOff(self):
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOff(), 0)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOffMin(), 0)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOffMax(), 2.5)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOffStepping(), 0.5)

    def test_setDomesticHotWaterHysteresis(self):
        self.device.setDomesticHotWaterHysteresis(5)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'heating.dhw.temperature.hysteresis')
        self.assertEqual(
            self.service.setPropertyData[0]['action'], 'setHysteresis')
        self.assertEqual(self.service.setPropertyData[0]['data'], {
                         'hysteresis': 5})

    def test_setDomesticHotWaterHysteresisSwitchOn(self):
        self.device.setDomesticHotWaterHysteresisSwitchOn(5)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'heating.dhw.temperature.hysteresis')
        self.assertEqual(
            self.service.setPropertyData[0]['action'], 'setHysteresisSwitchOnValue')
        self.assertEqual(self.service.setPropertyData[0]['data'], {
                         'hysteresis': 5})

    def test_setDomesticHotWaterHysteresisSwitchOff(self):
        self.device.setDomesticHotWaterHysteresisSwitchOff(5)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'heating.dhw.temperature.hysteresis')
        self.assertEqual(
            self.service.setPropertyData[0]['action'], 'setHysteresisSwitchOffValue')
        self.assertEqual(self.service.setPropertyData[0]['data'], {
                         'hysteresis': 5})

    def test_getDomesticHotWaterStorageTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterStorageTemperature(), 46.8)

    def test_getSupplyPressure(self):
        self.assertEqual(self.device.getSupplyPressure(), 1.8)
        self.assertEqual(self.device.getSupplyPressureUnit(), "bar")

    def test_getSeasonalPerformanceFactor(self):
        self.assertEqual(self.device.getSeasonalPerformanceFactorDHW(), 3.8)
        self.assertEqual(self.device.getSeasonalPerformanceFactorHeating(), 3.9)
        self.assertEqual(self.device.getSeasonalPerformanceFactorTotal(), 3.9)

    def test_getHeatingRod(self):
        self.assertEqual(self.device.getHeatingRodStarts(), 314)
        self.assertEqual(self.device.getHeatingRodHours(), 31)

    def test_getHeatingRodPowerConsumptionSummaryDHW(self):
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryDHWUnit(), "kilowattHour")
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryDHWCurrentDay(), 0)
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryDHWCurrentMonth(), 0)
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryDHWCurrentYear(), 3.3)
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryDHWLastMonth(), 0)
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryDHWLastSevenDays(), 0)
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryDHWLastYear(), 28)

    def test_getHeatingRodPowerConsumptionSummaryHeating(self):
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryHeatingUnit(), "kilowattHour")
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryHeatingCurrentDay(), 0)
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryHeatingCurrentMonth(), 0)
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryHeatingCurrentYear(), 29.5)
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryHeatingLastMonth(), 0)
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryHeatingLastSevenDays(), 0)
        self.assertEqual(
            self.device.getHeatingRodPowerConsumptionSummaryHeatingLastYear(), 53.6)

    def test_inverter_getCurrent(self):
        self.assertEqual(self.device.inverters[0].getCurrent(), 0)

    def test_inverter_getPower(self):
        self.assertEqual(self.device.inverters[0].getPower(), 0)

    def test_inverter_getTemperature(self):
        self.assertEqual(self.device.inverters[0].getTemperature(), 26.3)

    def test_getDomesticHotWaterOperatingModes(self):
        self.assertListEqual(
            self.device.getDomesticHotWaterOperatingModes(),
            ['efficientWithMinComfort', 'efficient', 'off'])

    def test_getDomesticHotWaterActiveOperatingMode(self):
        self.assertEqual(
            self.device.getDomesticHotWaterActiveOperatingMode(), 'efficient')

    def test_getWifiSignalStrength(self):
        self.assertEqual(self.device.getWifiSignalStrength(), -30)

    def test_compressor_getSpeed(self):
        self.assertEqual(self.device.getCompressor(0).getSpeed(), 0)
        self.assertEqual(self.device.getCompressor(0).getSpeedUnit(), "revolutionsPerSecond")

    def test_circuit_getTargetTemperature(self):
        self.assertEqual(self.device.circuits[0].getTargetTemperature(), 30)

    def test_getDefrostingActive(self):
        self.assertFalse(self.device.getDefrostingActive())

    def test_getFourThreeWayValvePosition(self):
        self.assertEqual(self.device.getFourThreeWayValvePosition(), "climatCircuitTwoDefrost")

    def test_getSecondaryCircuitOperationState(self):
        self.assertEqual(self.device.getSecondaryCircuitOperationState(), "standby")
        self.assertEqual(self.device.getSecondaryCircuitOperationStateTarget(), "standby")

    def test_getSecondaryCircuitFourThreeWayValvePosition(self):
        self.assertEqual(self.device.getSecondaryCircuitFourThreeWayValvePosition(), 52)
        self.assertEqual(self.device.getSecondaryCircuitFourThreeWayValvePositionTarget(), 50)
        self.assertEqual(self.device.getSecondaryCircuitFourThreeWayValvePositionUnit(), "percent")

    def test_getPowerConsumptionLimit(self):
        self.assertEqual(self.device.getPowerConsumptionLimit(), 0)
        self.assertEqual(self.device.getPowerConsumptionLimitUnit(), "watt")
        self.assertEqual(self.device.getPowerConsumptionLimitStatus(), "unlimitedAutonomous")

    def test_getPowerConsumptionLimitationSource(self):
        self.assertEqual(self.device.getPowerConsumptionLimitationSource(), "14aOff")

    def test_getHeatProductionSummaryHeating(self):
        self.assertEqual(self.device.getHeatProductionSummaryHeatingUnit(), "kilowattHour")
        self.assertEqual(self.device.getHeatProductionSummaryHeatingCurrentDay(), 22.8)
        self.assertEqual(self.device.getHeatProductionSummaryHeatingCurrentMonth(), 164.3)
        self.assertEqual(self.device.getHeatProductionSummaryHeatingCurrentYear(), 10024.2)
        self.assertEqual(self.device.getHeatProductionSummaryHeatingLastMonth(), 183.1)
        self.assertEqual(self.device.getHeatProductionSummaryHeatingLastSevenDays(), 206.3)
        self.assertEqual(self.device.getHeatProductionSummaryHeatingLastYear(), 15472.4)

    def test_getHeatProductionSummaryDomesticHotWater(self):
        self.assertEqual(self.device.getHeatProductionSummaryDomesticHotWaterUnit(), "kilowattHour")
        self.assertEqual(self.device.getHeatProductionSummaryDomesticHotWaterCurrentDay(), 9.6)
        self.assertEqual(self.device.getHeatProductionSummaryDomesticHotWaterCurrentMonth(), 61.8)
        self.assertEqual(self.device.getHeatProductionSummaryDomesticHotWaterCurrentYear(), 3382.9)
        self.assertEqual(self.device.getHeatProductionSummaryDomesticHotWaterLastMonth(), 389.9)
        self.assertEqual(self.device.getHeatProductionSummaryDomesticHotWaterLastSevenDays(), 96.7)
        self.assertEqual(self.device.getHeatProductionSummaryDomesticHotWaterLastYear(), 5903.8)
