import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal250A(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal250A.json')
        self.device = HeatPump(self.service)

    def test_getCompressorActive(self):
        self.assertEqual(self.device.compressors[0].getActive(), True)

    def test_getCompressorHours(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHours(), 1223)

    def test_getCompressorStarts(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getStarts(), 354)

    def test_getHeatingCurveSlope(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveSlope(), 0.8)

    def test_getHeatingCurveShift(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveShift(), 0)

    def test_getReturnTemperature(self):
        self.assertAlmostEqual(self.device.getReturnTemperature(), 31.6)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 5.9)

    def test_getPrograms(self):
        expected_programs = ['comfortCooling', 'comfortCoolingEnergySaving', 'comfortEnergySaving', 'comfortHeating', 'fixed', 'forcedLastFromSchedule', 'frostprotection', 'normalCooling', 'normalCoolingEnergySaving', 'normalEnergySaving', 'normalHeating', 'reducedCooling', 'reducedCoolingEnergySaving', 'reducedEnergySaving', 'reducedHeating', 'standby', 'summerEco']
        self.assertListEqual(
            self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['standby', 'heating', 'dhw', 'dhwAndHeating']
        self.assertListEqual(
            self.device.circuits[0].getModes(), expected_modes)

    def test_getPowerConsumptionUnit(self):
        self.assertEqual(
            self.device.getPowerConsumptionUnit(), "kilowattHour")

    def test_getPowerConsumptionToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionToday(), 6.9)

    def test_getPowerConsumptionDomesticHotWaterToday(self):
        self.assertAlmostEqual(
            self.device.getPowerConsumptionDomesticHotWaterToday(), 1.0)

    def test_getPowerSummaryConsumptionHeatingCurrentDay(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentDay(), 5.9)

    def test_getPowerSummaryConsumptionHeatingCurrentMonth(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentMonth(), 48)

    def test_getPowerSummaryConsumptionHeatingCurrentYear(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentYear(), 48)

    def test_getPowerSummaryConsumptionHeatingLastMonth(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingLastMonth(), 463.9)

    def test_getPowerSummaryConsumptionHeatingLastSevenDays(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingLastSevenDays(), 41.4)

    def test_getPowerSummaryConsumptionHeatingLastYear(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingLastYear(), 882.1)

    def test_getPowerSummaryConsumptionHeatingUnit(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingUnit(), "kilowattHour")

    def test_getBufferMainTemperature(self):
        self.assertAlmostEqual(
            self.device.getBufferMainTemperature(), 31.9)

    def test_getOutsideTemperature(self):
        self.assertEqual(
            self.device.getOutsideTemperature(), 6.1)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getPowerSummaryConsumptionDomesticHotWaterUnit(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterUnit(), "kilowattHour")

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentDay(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentDay(), 1.0)

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(), 18.0)

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentYear(), 18.0)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastMonth(), 74.8)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(), 14.0)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastYear(), 177.7)

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
