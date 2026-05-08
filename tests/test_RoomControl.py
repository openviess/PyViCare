import unittest

from PyViCare.PyViCareRoomControl import RoomControl
from tests.ViCareServiceMock import ViCareServiceMock


class RoomControlTest(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/RoomControl.json')
        self.device = RoomControl(self.service)

    def test_getAvailableRooms(self):
        rooms = self.device.getAvailableRooms()
        self.assertIn("0", rooms)
        self.assertEqual(len(rooms), 10)

    def test_getRoomActorIds(self):
        actors = self.device.getRoomActorIds("0")
        self.assertIsInstance(actors, list)
        self.assertTrue(len(actors) > 0)

    def test_getRoomName(self):
        self.assertEqual(self.device.getRoomName("0"), "Bedroom")
        self.assertEqual(self.device.getRoomName("4"), "Living Room")

    def test_getRoomType(self):
        self.assertEqual(self.device.getRoomType("0"), "bedroom")
        self.assertEqual(self.device.getRoomType("4"), "livingroom")

    def test_getRoomTemperature(self):
        self.assertAlmostEqual(self.device.getRoomTemperature("0"), 20.7)

    def test_getRoomHumidity(self):
        self.assertEqual(self.device.getRoomHumidity("0"), 53)

    def test_getRoomCondensationRisk(self):
        result = self.device.getRoomCondensationRisk("0")
        self.assertIsNotNone(result)

    def test_getRoomOperatingStateLevel(self):
        result = self.device.getRoomOperatingStateLevel("0")
        self.assertIsNotNone(result)

    def test_getRoomNormalHeatingTemperature(self):
        temp = self.device.getRoomNormalHeatingTemperature("0")
        self.assertIsInstance(temp, (int, float))

    def test_getRoomReducedHeatingTemperature(self):
        temp = self.device.getRoomReducedHeatingTemperature("0")
        self.assertIsInstance(temp, (int, float))

    def test_getRoomComfortHeatingTemperature(self):
        temp = self.device.getRoomComfortHeatingTemperature("0")
        self.assertIsInstance(temp, (int, float))

    def test_getRoomSchedule(self):
        schedule = self.device.getRoomSchedule("0")
        self.assertIn("active", schedule)
        self.assertIn("mon", schedule)

    def test_getRoomManualTillNextScheduleActive(self):
        result = self.device.getRoomManualTillNextScheduleActive("0")
        self.assertIsInstance(result, bool)
