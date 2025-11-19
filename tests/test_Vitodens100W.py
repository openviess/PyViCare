import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens100W(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitodens100W.json')
        self.device = GazBoiler(self.service)

    def test_getActive(self):
        self.assertEqual(self.device.burners[0].getActive(), True)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.burners[0].getStarts(), 18187)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.burners[0].getHours(), 5598)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.burners[0].getModulation(), 86.9)

    def test_getGasSummaryConsumptionHeatingCurrentDay(self):
        self.assertEqual(self.device.getGasSummaryConsumptionHeatingCurrentDay(), 1.6)
        self.assertEqual(self.device.getGasSummaryConsumptionHeatingUnit(), "cubicMeter")

    def test_getGasSummaryConsumptionDomesticHotWaterCurrentMonth(self):
        self.assertEqual(self.device.getGasSummaryConsumptionDomesticHotWaterCurrentMonth(), 0.8)
        self.assertEqual(self.device.getGasSummaryConsumptionDomesticHotWaterUnit(), "cubicMeter")

    def test_getPowerSummaryConsumptionHeatingCurrentDay(self):
        self.assertEqual(self.device.getPowerSummaryConsumptionHeatingCurrentDay(), 0.1)
        self.assertEqual(self.device.getPowerSummaryConsumptionHeatingUnit(), "kilowattHour")

    def test_getPowerSummaryConsumptionDomesticHotWaterCurrentYear(self):
        self.assertEqual(self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentYear(), 1.4)
        self.assertEqual(self.device.getPowerSummaryConsumptionDomesticHotWaterUnit(), "kilowattHour")

    def test_getGasSummaryConsumptionDomesticHotWaterUnit(self):
        self.assertEqual(self.device.getGasSummaryConsumptionDomesticHotWaterUnit(), "cubicMeter")
