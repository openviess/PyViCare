import unittest

from PyViCare.PyViCareRoomControl import RoomControl
from tests.ViCareServiceMock import ViCareServiceMock


class RoomControlTest(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/RoomControl.json')
        self.device = RoomControl(self.service)

    def test_getRoomTemperature(self):
        self.assertAlmostEqual(self.device.getRoomTemperature("0"), 23.4)
        self.assertAlmostEqual(self.device.getRoomTemperature("1"), 22.8)

    def test_getRoomHumidity(self):
        self.assertEqual(self.device.getRoomHumidity("0"), 49)
        self.assertEqual(self.device.getRoomHumidity("1"), 56)

    def test_getRoomCO2(self):
        self.assertEqual(self.device.getRoomCO2("0"), 1000)
        self.assertEqual(self.device.getRoomCO2("1"), 850)

    def test_getRoomCondensationRisk(self):
        self.assertFalse(self.device.getRoomCondensationRisk("0"))
        self.assertFalse(self.device.getRoomCondensationRisk("1"))
