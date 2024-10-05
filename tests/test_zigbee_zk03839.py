import unittest

from PyViCare.PyViCareRoomSensor import RoomSensor
from tests.ViCareServiceMock import ViCareServiceMock


class ZK03839(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/zigbee_zk03839.json')
        self.device = RoomSensor(self.service)

    def test_isDomesticHotWaterDevice(self):
        self.assertFalse(self.device.isDomesticHotWaterDevice())

    def test_isSolarThermalDevice(self):
        self.assertFalse(self.device.isSolarThermalDevice())

    def test_isVentilationDevice(self):
        self.assertFalse(self.device.isVentilationDevice())

    def test_getTemperature(self):
        self.assertEqual(
            self.device.getTemperature(), 19.7)

    def test_getHumidity(self):
        self.assertEqual(
            self.device.getHumidity(), 56)
