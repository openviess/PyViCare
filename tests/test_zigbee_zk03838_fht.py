import unittest

from PyViCare.PyViCareFloorHeating import FloorHeating
from tests.ViCareServiceMock import ViCareServiceMock


class ZK03840(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/zigbee_fht.json')
        self.device = FloorHeating(self.service)

    def test_getSerial(self):
        self.assertEqual(
            self.device.getSerial(), "zigbee-5cc7c1fffea25f73")

    def test_getActiveMode(self):
        self.assertEqual(
            self.device.getActiveMode(), "standby")
