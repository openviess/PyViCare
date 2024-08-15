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
        self.assertAlmostEqual(
            self.device.compressors[0].getHours(), 3869)

    def test_getCompressorStarts(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getStarts(), 668)

    def test_getCompressorPhase(self):
        self.assertEqual(
            self.device.getCompressor(0).getPhase(), "ready")

    def test_getHeatingCurveSlope(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveSlope(), 0.6)

    def test_getHeatingCurveShift(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveShift(), 6)

    def test_getReturnTemperature(self):
        self.assertAlmostEqual(self.device.getReturnTemperature(), 25.4)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 38.5)

    def test_getPrograms(self):
        expected_programs = ['comfortCooling', 'comfortCoolingEnergySaving', 'comfortEnergySaving', 'comfortHeating', 'eco', 'fixed', 'forcedLastFromSchedule', 'frostprotection', 'normalCooling', 'normalCoolingEnergySaving', 'normalEnergySaving', 'normalHeating', 'reducedCooling', 'reducedCoolingEnergySaving', 'reducedEnergySaving', 'reducedHeating', 'standby']
        self.assertListEqual(
            expected_programs, self.device.circuits[0].getPrograms())

    def test_getModes(self):
        expected_modes = ['heating', 'standby']
        self.assertListEqual(
            expected_modes, self.device.circuits[0].getModes())

    def test_getPowerConsumptionUnit(self):
        self.assertEqual(
            self.device.getPowerConsumptionUnit(), "kilowattHour")

    def test_getPowerConsumptionToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionToday(), 0)

    def test_getPowerConsumptionDomesticHotWaterToday(self):
        self.assertAlmostEqual(
            self.device.getPowerConsumptionDomesticHotWaterToday(), 0)

    def test_getPowerSummaryConsumptionHeatingUnit(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionHeatingUnit(), "kilowattHour")

    def test_getPowerSummaryConsumptionHeatingCurrentDay(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentDay(), 0)

    def test_getPowerSummaryConsumptionHeatingCurrentMonth(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentMonth(), 0)

    def test_getPowerSummaryConsumptionHeatingCurrentYear(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingCurrentYear(), 2191.7999999999997)

    def test_getPowerSummaryConsumptionHeatingLastMonth(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingLastMonth(), 0)

    def test_getPowerSummaryConsumptionHeatingLastSevenDays(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingLastSevenDays(), 0)

    def test_getPowerSummaryConsumptionHeatingLastYear(self):
        self.assertAlmostEqual(
            self.device.getPowerSummaryConsumptionHeatingLastYear(), 1460.6)

    def test_getPowerSummaryConsumptionDomesticHotWaterUnit(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterUnit(), "kilowattHour")

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentDay(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentDay(), 0)

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(), 11.4)

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentYear(), 931.3)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastMonth(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastMonth(), 45.7)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(), 5.7)

    def test_getPowerSummaryConsumptionDomesticHotWaterLastYear(self):
        self.assertEqual(
            self.device.getPowerSummaryConsumptionDomesticHotWaterLastYear(), 557.2)

    def test_getBufferMainTemperature(self):
        self.assertAlmostEqual(
            self.device.getBufferMainTemperature(), 23.4)

    def test_getOutsideTemperature(self):
        self.assertEqual(
            self.device.getOutsideTemperature(), 22.4)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)
