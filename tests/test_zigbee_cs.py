import unittest

from PyViCare.PyViCareRoomSensor import RoomSensor
from tests.ViCareServiceMock import ViCareServiceMock


class ZK03839(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/zigbee_Smart_cs_generic_50.json')
        self.device = RoomSensor(self.service)

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), "zigbee-f082c0fffe43d8cd")

    def test_isDomesticHotWaterDevice(self):
        self.assertEqual(self.device.isDomesticHotWaterDevice(), False)

    def test_isSolarThermalDevice(self):
        self.assertEqual(self.device.isSolarThermalDevice(), False)

    def test_isVentilationDevice(self):
        self.assertEqual(self.device.isVentilationDevice(), False)

    def test_getTemperature(self):
        self.assertEqual(self.device.getTemperature(), 15)

    def test_getHumidity(self):
        self.assertEqual(self.device.getHumidity(), 37)

    def test_getBatteryLevel(self):
        self.assertEqual(self.device.getBatteryLevel(), 89)
