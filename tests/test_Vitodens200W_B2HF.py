import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens200W_B2HF(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitodens200W_B2HF.json')
        self.device = GazBoiler(self.service)

    def test_getSupplyPressure(self):
        self.assertEqual(self.device.getSupplyPressure(), 1.5)

    def test_getSupplyPressureUnit(self):
        self.assertEqual(self.device.getSupplyPressureUnit(), 'bar')

    # Total power consumption:
    def test_getPowerConsumptionUnit(self):
        self.assertEqual(
            self.device.getPowerConsumptionUnit(), "kilowattHour")

    def test_getPowerConsumptionToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionToday(), 0)

    def test_getPowerConsumptionThisMonth(self):
        self.assertEqual(
            self.device.getPowerConsumptionThisMonth(), 6.0)

    def test_getPowerConsumptionThisYear(self):
        self.assertEqual(
            self.device.getPowerConsumptionThisYear(), 90.39999999999999)

    # Power consumption for Domestic Hot Water:
    def test_getPowerConsumptionDomesticHotWaterUnit(self):
        self.assertEqual(
            self.device.getPowerConsumptionDomesticHotWaterUnit(), "kilowattHour")

    def test_getPowerConsumptionDomesticHotWaterToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionDomesticHotWaterToday(), 0)

    def test_getPowerConsumptionDomesticHotWaterThisMonth(self):
        self.assertEqual(
            self.device.getPowerConsumptionDomesticHotWaterThisMonth(), 1.3)

    def test_getPowerConsumptionDomesticHotWaterThisYear(self):
        self.assertEqual(
            self.device.getPowerConsumptionDomesticHotWaterThisYear(), 10.6)

    # Power consumption for Heating:
    def test_getPowerConsumptionHeatingUnit(self):
        self.assertEqual(
            self.device.getPowerConsumptionHeatingUnit(), "kilowattHour")

    def test_getPowerConsumptionHeatingToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionHeatingToday(), 0.4)

    def test_getPowerConsumptionHeatingThisMonth(self):
        self.assertEqual(
            self.device.getPowerConsumptionHeatingThisMonth(), 5.1)

    def test_getPowerConsumptionHeatingThisYear(self):
        self.assertEqual(
            self.device.getPowerConsumptionHeatingThisYear(), 79.8)
