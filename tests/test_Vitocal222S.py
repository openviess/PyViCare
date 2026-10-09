import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal222S(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/Vitocal222S.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_condensers_getLiquidTemperature(self):
        self.assertEqual(self.device.getCondensor(0).getLiquidTemperature(), 26.1)
        self.assertEqual(self.device.getCondensor(0).getLiquidTemperatureUnit(), "celsius")

    def test_compressor_getInletTemperature(self):
        self.assertEqual(self.device.getCompressor(0).getInletTemperature(), 0.0)
        self.assertEqual(self.device.getCompressor(0).getInletTemperatureUnit(), "celsius")

    def test_compressor_getOutletTemperature(self):
        self.assertEqual(self.device.getCompressor(0).getOutletTemperature(), 32.8)
        self.assertEqual(self.device.getCompressor(0).getOutletTemperatureUnit(), "celsius")

    def test_compressor_getSpeed(self):
        self.assertEqual(self.device.getCompressor(0).getSpeed(), 20)

    def test_getDomesticHotWaterOperatingModes(self):
        self.assertListEqual(
            self.device.getDomesticHotWaterOperatingModes(),
            ['efficientWithMinComfort', 'efficient', 'off'])

    def test_getDomesticHotWaterActiveOperatingMode(self):
        self.assertEqual(
            self.device.getDomesticHotWaterActiveOperatingMode(), 'efficient')

    def test_getHoliday(self):
        self.assertFalse(self.device.getHolidayActive())
        self.assertEqual(self.device.getHolidayStart(), "2023-07-09")
        self.assertEqual(self.device.getHolidayEnd(), "2023-07-21")

    def test_getHolidayAtHome_unset(self):
        self.assertFalse(self.device.getHolidayAtHomeActive())
        self.assertIsNone(self.device.getHolidayAtHomeStart())
        self.assertIsNone(self.device.getHolidayAtHomeEnd())

    def test_scheduleHoliday(self):
        self.device.scheduleHoliday("2026-10-08", "2026-10-09")
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'heating.operating.programs.holiday')
        self.assertEqual(self.service.setPropertyData[0]['action'], 'schedule')
        self.assertEqual(self.service.setPropertyData[0]['data'], {'start': '2026-10-08', 'end': '2026-10-09'})

    def test_changeHolidayEndDate(self):
        self.device.changeHolidayEndDate("2026-10-10")
        self.assertEqual(self.service.setPropertyData[0]['action'], 'changeEndDate')
        self.assertEqual(self.service.setPropertyData[0]['data'], {'end': '2026-10-10'})

    def test_unscheduleHolidayAtHome(self):
        self.device.unscheduleHolidayAtHome()
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'heating.operating.programs.holidayAtHome')
        self.assertEqual(self.service.setPropertyData[0]['action'], 'unschedule')
        self.assertEqual(self.service.setPropertyData[0]['data'], {})
