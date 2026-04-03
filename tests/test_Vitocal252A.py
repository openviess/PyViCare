import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal252A(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal252A.json')
        self.device = HeatPump(self.service)

    def test_compressor_getActive(self):
        self.assertTrue(self.device.compressors[0].getActive())

    def test_compressor_getHours(self):
        self.assertEqual(
            self.device.compressors[0].getHours(), 582)

    def test_compressor_getStarts(self):
        self.assertEqual(
            self.device.compressors[0].getStarts(), 836)

    def test_compressor_getPowerConsumptionThisYear(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.compressors[0].getPowerConsumptionCoolingThisYear)

    def test_compressor_getPowerConsumptionCoolingThisYear(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.getPowerConsumptionCoolingThisYear)

    def test_getHeatingCurveSlope(self):
        self.assertEqual(
            self.device.circuits[0].getHeatingCurveSlope(), 0.6)

    def test_getHeatingCurveShift(self):
        self.assertEqual(
            self.device.circuits[0].getHeatingCurveShift(), 0)

    def test_getReturnTemperature(self):
        self.assertEqual(self.device.getReturnTemperature(), 39.3)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 3.0)

    def test_getPrograms(self):
        expected_programs = ['comfortCooling', 'comfortCoolingEnergySaving', 'comfortEnergySaving', 'comfortHeating', 'fixed', 'forcedLastFromSchedule', 'frostprotection', 'normalCooling', 'normalCoolingEnergySaving', 'normalEnergySaving', 'normalHeating', 'reducedCooling', 'reducedCoolingEnergySaving', 'reducedEnergySaving', 'reducedHeating', 'standby']
        self.assertListEqual(expected_programs, self.device.circuits[0].getPrograms())

    def test_getModes(self):
        expected_modes = ['heating', 'standby']
        self.assertListEqual(expected_modes, self.device.circuits[0].getModes())

    # Total power consumption:
    def test_getPowerConsumptionUnit(self):
        self.assertEqual(
            self.device.getPowerConsumptionUnit(), "kilowattHour")

    def test_getPowerConsumptionToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionToday(), 13.0)

    def test_getPowerConsumptionThisMonth(self):
        self.assertEqual(
            self.device.getPowerConsumptionThisMonth(), 176.10000000000002)

    def test_getPowerConsumptionThisYear(self):
        self.assertEqual(
            self.device.getPowerConsumptionThisYear(), 478.6)

    # Power consumption for Domestic Hot Water:
    def test_getPowerConsumptionDomesticHotWaterUnit(self):
        self.assertEqual(
            self.device.getPowerConsumptionDomesticHotWaterUnit(), "kilowattHour")

    def test_getPowerConsumptionDomesticHotWaterToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionDomesticHotWaterToday(), 2.3)

    def test_getPowerConsumptionDomesticHotWaterThisMonth(self):
        self.assertEqual(
            self.device.getPowerConsumptionDomesticHotWaterThisMonth(), 45.2)

    def test_getPowerConsumptionDomesticHotWaterThisYear(self):
        self.assertEqual(
            self.device.getPowerConsumptionDomesticHotWaterThisYear(), 215.4)

    # Power consumption for Heating:
    def test_getPowerConsumptionHeatingUnit(self):
        self.assertEqual(
            self.device.getPowerConsumptionHeatingUnit(), "kilowattHour")

    def test_getPowerConsumptionHeatingToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionHeatingToday(), 10.7)

    def test_getPowerConsumptionHeatingThisMonth(self):
        self.assertEqual(
            self.device.getPowerConsumptionHeatingThisMonth(), 130.9)

    def test_getPowerConsumptionHeatingThisYear(self):
        self.assertEqual(
            self.device.getPowerConsumptionHeatingThisYear(), 263.2)

    # Power summary consumption for Heating:
    def test_getPowerSummaryConsumptionHeatingCurrentDay(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentDay(), 10.7)

    def test_getPowerSummaryConsumptionHeatingCurrentMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentMonth(), 130.9)

    def test_getPowerSummaryConsumptionHeatingCurrentYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentYear(), 263.2)

    def test_getPowerSummaryConsumptionHeatingLastMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingLastMonth(), 97.8)

    def test_getPowerSummaryConsumptionHeatingLastSevenDays(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingLastSevenDays(), 51.7)

    def test_getPowerSummaryConsumptionHeatingLastYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingLastYear(), 0)

    def test_getPowerSummaryConsumptionHeatingUnit(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingUnit(), "kilowattHour")

    def test_getBufferMainTemperature(self):
        self.assertRaises(PyViCareNotSupportedFeatureError, self.device.getBufferMainTemperature)

    def test_getOutsideTemperature(self):
        self.assertEqual(
            self.device.getOutsideTemperature(), 3.3)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getPowerSummaryConsumptionDomesticHotWaterUnit(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterUnit(), "kilowattHour")

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentDay(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentDay(), 2.3)

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(), 45.2)

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentYear(), 215.4)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastMonth(), 70.5)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(), 16.7)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastYear(), 0)

    def test_compressor_getPhase(self):
        self.assertEqual(
            self.device.getCompressor(0).getPhase(), "ready")

    def test_getDomesticHotWaterHysteresis(self):
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisUnit(), 'kelvin')
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresis(), 6)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisMin(), 1)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisMax(), 10)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisStepping(), 0.5)

    def test_getDomesticHotWaterHysteresisSwitchOn(self):
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOn(), 6)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOnMin(), 1)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOnMax(), 10)
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOnStepping(), 0.5)

    def test_getDomesticHotWaterHysteresisSwitchOff(self):
        self.assertEqual(
            self.device.getDomesticHotWaterHysteresisSwitchOff(), 2.0)
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
            self.device.getDomesticHotWaterStorageTemperature(), 35.6)

    def test_getSupplyPressure(self):
        self.assertEqual(self.device.getSupplyPressure(), 1.6)
        self.assertEqual(self.device.getSupplyPressureUnit(), "bar")

    def test_getSeasonalPerformanceFactor(self):
        self.assertEqual(self.device.getSeasonalPerformanceFactorDHW(), 5.2)
        self.assertEqual(self.device.getSeasonalPerformanceFactorHeating(), 7.1)
        self.assertEqual(self.device.getSeasonalPerformanceFactorTotal(), 6.0)

    def test_getHeatingRod(self):
        self.assertEqual(self.device.getHeatingRodStarts(), 1)
        self.assertEqual(self.device.getHeatingRodHours(), 0)
