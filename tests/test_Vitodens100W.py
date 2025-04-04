import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens100W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitodens100W.json')
        self.device = GazBoiler(self.service)

    def test_getActive(self):
        self.assertEqual(self.device.burners[0].getActive(), False)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.burners[0].getStarts(), 6826)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.burners[0].getHours(), 675)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.burners[0].getModulation(), 0)

    def test_getGasSummaryConsumptionHeatingCurrentDay(self):
        self.assertEqual(self.device.getGasSummaryConsumptionHeatingCurrentDay(), 11.2)
        self.assertEqual(self.device.getGasSummaryConsumptionHeatingUnit(), "cubicMeter")

    def test_getGasSummaryConsumptionDomesticHotWaterCurrentMonth(self):
        self.assertEqual(self.device.getGasSummaryConsumptionDomesticHotWaterCurrentMonth(), 13.7)
        self.assertEqual(self.device.getGasSummaryConsumptionDomesticHotWaterUnit(), "cubicMeter")

    def test_getPowerSummaryConsumptionHeatingCurrentDay(self):
        self.assertEqual(self.device.getPowerSummaryConsumptionHeatingCurrentDay(), 0.9)
        self.assertEqual(self.device.getPowerSummaryConsumptionHeatingUnit(), "kilowattHour")

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentYear(self):
        self.assertEqual(self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentYear(), 18)
        self.assertEqual(self.device.getPowerSummaryConsumptionDomesticHotWaterUnit(), "kilowattHour")

    def test_getGasSummaryConsumptionDomesticHotWaterUnit(self):
        self.assertEqual(self.device.getGasSummaryConsumptionDomesticHotWaterUnit(), "cubicMeter")
