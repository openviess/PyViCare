import unittest

from PyViCare.PyViCareRoomControl import RoomControl
from PyViCare.PyViCareRoomSensor import RoomSensor
from PyViCare.PyViCareUtils import (
    PyViCareCommandError,
    PyViCareNotSupportedFeatureError,
    isSupported,
)
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

    def test_buildActorRoomMap(self):
        actor_map = self.device.buildActorRoomMap()
        self.assertIsInstance(actor_map, dict)
        self.assertTrue(len(actor_map) > 0)
        for room_id in actor_map.values():
            self.assertIsInstance(room_id, str)


class RoomSensorEnrichmentTest(unittest.TestCase):
    def setUp(self):
        self.room_control_service = ViCareServiceMock('response/RoomControl.json')
        self.room_control = RoomControl(self.room_control_service)
        self.sensor_service = ViCareServiceMock('response/RoomControl.json',
                                                rawInput={"data": []})
        self.sensor = RoomSensor(self.sensor_service)
        self.sensor.setRoomControl(self.room_control, "0")

    def test_getTemperature(self):
        self.assertAlmostEqual(self.sensor.getTemperature(), 20.7)

    def test_getHumidity(self):
        self.assertEqual(self.sensor.getHumidity(), 53)

    def test_getRoomName(self):
        self.assertEqual(self.sensor.getRoomName(), "Bedroom")

    def test_getRoomType(self):
        self.assertEqual(self.sensor.getRoomType(), "bedroom")

    def test_getCondensationRisk(self):
        result = self.sensor.getCondensationRisk()
        self.assertIsNotNone(result)

    def test_getOperatingStateLevel(self):
        result = self.sensor.getOperatingStateLevel()
        self.assertIsNotNone(result)

    def test_getNormalHeatingTemperature(self):
        temp = self.sensor.getNormalHeatingTemperature()
        self.assertIsInstance(temp, (int, float))

    def test_getReducedHeatingTemperature(self):
        temp = self.sensor.getReducedHeatingTemperature()
        self.assertIsInstance(temp, (int, float))

    def test_getComfortHeatingTemperature(self):
        temp = self.sensor.getComfortHeatingTemperature()
        self.assertIsInstance(temp, (int, float))

    def test_getSchedule(self):
        schedule = self.sensor.getSchedule()
        self.assertIn("active", schedule)
        self.assertIn("mon", schedule)

    def test_getManualTillNextScheduleActive(self):
        result = self.sensor.getManualTillNextScheduleActive()
        self.assertIsInstance(result, bool)

    def test_without_enrichment_reports_not_supported(self):
        sensor = RoomSensor(self.sensor_service)
        self.assertFalse(isSupported(sensor.getRoomName))
        self.assertFalse(isSupported(sensor.getNormalHeatingTemperature))

        with self.assertRaises(PyViCareNotSupportedFeatureError):
            sensor.getRoomName()

        with self.assertRaises(PyViCareNotSupportedFeatureError):
            sensor.getNormalHeatingTemperature()

        with self.assertRaises(PyViCareCommandError):
            sensor.setNormalHeatingTemperature(20)
