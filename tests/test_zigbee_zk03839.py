import unittest

from PyViCare.PyViCareRoomSensor import RoomSensor
from tests.ViCareServiceMock import ViCareServiceMock

ROLES = [
    "type:E3",
    "type:climateSensor",
    "type:sensor",
    "type:smartRoomDevice"
]

class ZK03839(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock(ROLES, 'response/zigbee_zk03839.json')
        self.device = RoomSensor(self.service)

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), "zigbee-2c1165fffe977770")

    def test_isDomesticHotWaterDevice(self):
        self.assertEqual(self.device.isDomesticHotWaterDevice(), False)

    def test_isSolarThermalDevice(self):
        self.assertEqual(self.device.isSolarThermalDevice(), False)

    def test_isVentilationDevice(self):
        self.assertEqual(self.device.isVentilationDevice(), False)

    def test_getTemperature(self):
        self.assertEqual(
            self.device.getTemperature(), 19.7)

    def test_getHumidity(self):
        self.assertEqual(
            self.device.getHumidity(), 56)
