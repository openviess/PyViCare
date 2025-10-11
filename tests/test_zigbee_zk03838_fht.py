import unittest

from PyViCare.PyViCareFloorHeating import FloorHeating, FloorHeatingChannel
from tests.ViCareServiceMock import ViCareServiceMock


class ZK03838MainViaHeatbox2(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/zigbee_zk03838_fht_main.json')
        self.device = FloorHeating(self.service)

    def test_getSerial(self):
        self.assertEqual(
            self.device.getSerial(), "zigbee-################")

    def test_getName(self):
        self.assertEqual(
            self.device.getName(), "EG Fußbodenthermostat")

    def test_getActiveMode(self):
        self.assertEqual(
            self.device.getActiveMode(), "heating")

    def test_getSupplyTemperature(self):
        self.assertEqual(
            self.device.getSupplyTemperature(), 31.0)

    def test_getZigbeeParentID(self):
        self.assertEqual(
            self.device.getZigbeeParentID(), "################")

    def test_getZigbeeSignalStrength(self):
        self.assertEqual(
            self.device.getZigbeeSignalStrength(), 37)

class ZK03838ChannelViaHeatbox2(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/zigbee_zk03838_fht_channel.json')
        self.device = FloorHeatingChannel(self.service)

    def test_getSerial(self):
        self.assertEqual(
            self.device.getSerial(), "zigbee-################-2")

    def test_getName(self):
        self.assertEqual(
            self.device.getName(), "Zone EG Bad")

    def test_getValvePosition(self):
        self.assertEqual(
            self.device.getValvePosition(), "closed")
