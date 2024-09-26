import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal250A(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal250A.json')
        self.device = HeatPump(self.service)

    def test_getCompressorActive(self):
        self.assertEqual(self.device.compressors[0].getActive(), False)

    def test_getCompressorHours(self):
        self.assertEqual(
            self.device.compressors[0].getHours(), 1090)

    def test_getCompressorStarts(self):
        self.assertEqual(
            self.device.compressors[0].getStarts(), 486)

    def test_getHeatingCurveSlope(self):
        self.assertEqual(
            self.device.circuits[0].getHeatingCurveSlope(), 0.6)

    def test_getHeatingCurveShift(self):
        self.assertEqual(
            self.device.circuits[0].getHeatingCurveShift(), 0)

    def test_getReturnTemperature(self):
        self.assertEqual(self.device.getReturnTemperature(), 31.6)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 16.9)

    def test_getPrograms(self):
        expected_programs = ['comfortCooling', 'comfortCoolingEnergySaving', 'comfortEnergySaving', 'comfortHeating', 'eco', 'fixed', 'forcedLastFromSchedule', 'frostprotection', 'normalCooling', 'normalCoolingEnergySaving', 'normalEnergySaving', 'normalHeating', 'reducedCooling', 'reducedCoolingEnergySaving', 'reducedEnergySaving', 'reducedHeating', 'standby']
        self.assertListEqual(expected_programs, self.device.circuits[0].getPrograms())

    def test_getModes(self):
        expected_modes = ['cooling', 'heating', 'heatingCooling', 'standby']
        self.assertListEqual(expected_modes, self.device.circuits[0].getModes())

    def test_getPowerConsumptionUnit(self):
        self.assertEqual(
            self.device.getPowerConsumptionUnit(), "kilowattHour")

    def test_getPowerConsumptionToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionToday(), 1.3)

    def test_getPowerConsumptionDomesticHotWaterToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionDomesticHotWaterToday(), 1.3)

    def test_getPowerSummaryConsumptionHeatingCurrentDay(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentDay(), 0)

    def test_getPowerSummaryConsumptionHeatingCurrentMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentMonth(), 0)

    def test_getPowerSummaryConsumptionHeatingCurrentYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentYear(), 529.4)

    def test_getPowerSummaryConsumptionHeatingLastMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingLastMonth(), 0)

    def test_getPowerSummaryConsumptionHeatingLastSevenDays(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingLastSevenDays(), 0)

    def test_getPowerSummaryConsumptionHeatingLastYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingLastYear(), 0)

    def test_getPowerSummaryConsumptionHeatingUnit(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingUnit(), "kilowattHour")

    @unittest.skip("dump is not up to date, underlying data point was rernamed")
    def test_getBufferMainTemperature(self):
        self.assertEqual(
            self.device.getBufferMainTemperature(), 31.9)

    def test_getOutsideTemperature(self):
        self.assertEqual(
            self.device.getOutsideTemperature(), 16.8)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getPowerSummaryConsumptionDomesticHotWaterUnit(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterUnit(), "kilowattHour")

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentDay(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentDay(), 1.3)

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(), 12.8)

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentYear(), 475)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastMonth(), 44.7)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(), 9.1)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastYear(), 0)

    def test_getCompressorPhase(self):
        self.assertEqual(
            self.device.getCompressor(0).getPhase(), "ready")

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
