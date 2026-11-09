import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal200(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/Vitocal151A.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_getPowerConsumptionCooling(self):
        self.assertEqual(self.device.getPowerConsumptionCoolingUnit(), "kilowattHour")
        self.assertEqual(self.device.getPowerConsumptionCoolingToday(), 0)
        self.assertEqual(self.device.getPowerConsumptionCoolingThisMonth(), 0.1)
        self.assertEqual(self.device.getPowerConsumptionCoolingThisYear(), 0.1)

    def test_getDomesticHotWaterHygieneEnabled(self):
        self.assertEqual(self.device.getDomesticHotWaterHygieneEnabled(), False)

    def test_getDomesticHotWaterHygieneNotSupported(self):
        # With the function switched off the device serves `enabled` alone, and
        # the trigger feature carries no properties at all.
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.getDomesticHotWaterHygieneActive)
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.getDomesticHotWaterHygieneTriggerStartHour)
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.getDomesticHotWaterHygieneTriggerStartMinute)
        self.assertRaises(PyViCareNotSupportedFeatureError,
                          self.device.getDomesticHotWaterHygieneTriggerWeekdays)

    def test_setDomesticHotWaterHygieneEnabledFallback(self):
        # This device serves only enable/disable, not setEnabled.
        self.device.setDomesticHotWaterHygieneEnabled(True)
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'heating.dhw.hygiene')
        self.assertEqual(self.service.setPropertyData[0]['action'], 'enable')
        self.assertEqual(self.service.setPropertyData[0]['data'], {})
