import unittest

from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareRoomSensor import RoomSensor
from tests.ViCareServiceMock import ViCareServiceMock


class ZK03839ViaHeatbox2(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "[device]")
        self.service = ViCareServiceMock('response/zigbee_zk03839_cs.json')
        self.device = RoomSensor(self.accessor, self.service)

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), "zigbee-################")

    def test_isDomesticHotWaterDevice(self):
        self.assertEqual(self.device.isDomesticHotWaterDevice(), False)

    def test_isSolarThermalDevice(self):
        self.assertEqual(self.device.isSolarThermalDevice(), False)

    def test_isVentilationDevice(self):
        self.assertEqual(self.device.isVentilationDevice(), False)

    def test_getTemperature(self):
        self.assertEqual(
            self.device.getTemperature(), 22.1)

    def test_getHumidity(self):
        self.assertEqual(
            self.device.getHumidity(), 41.3)
