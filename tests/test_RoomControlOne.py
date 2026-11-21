import unittest

from PyViCare.PyViCareRoomControl import Room, RoomControl
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class RoomControlOneTest(unittest.TestCase):
    """RoomControl One (E3_RoomControl_One_05).

    The dump differs from RoomControl.json in two ways that are worth
    covering: room 2 has neither a humidity nor a window sensor, so the
    not-supported paths are exercised against real data, and the installation
    serves the rooms.others branch, which no accessor reads yet.
    """

    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/RoomControlOne.json')
        self.device = RoomControl(self.accessor, self.service)

    def test_getAvailableRoomIds(self):
        self.assertEqual(self.device.getAvailableRoomIds(), ["0", "1", "2"])

    def test_getAvailableRoomIds_ignores_other_rooms(self):
        # rooms.others.0 is served by this installation but is not a room with
        # a climate function, so it must not appear among the room ids.
        self.assertNotIn("others.0", self.device.getAvailableRoomIds())

    def test_rooms(self):
        rooms = self.device.rooms
        self.assertEqual([room.id for room in rooms], ["0", "1", "2"])
        self.assertIsInstance(rooms[0], Room)
        self.assertAlmostEqual(rooms[0].getTemperature(), 20.4)
        self.assertAlmostEqual(rooms[1].getTemperature(), 20.5)
        self.assertAlmostEqual(rooms[2].getTemperature(), 19.4)

    def test_getRoomTemperature(self):
        self.assertAlmostEqual(self.device.getRoomTemperature("0"), 20.4)
        self.assertAlmostEqual(self.device.getRoomTemperature("1"), 20.5)
        self.assertAlmostEqual(self.device.getRoomTemperature("2"), 19.4)

    def test_getRoomHumidity(self):
        self.assertAlmostEqual(self.device.getRoomHumidity("0"), 53)
        self.assertAlmostEqual(self.device.getRoomHumidity("1"), 45)

    def test_getRoomHumidity_without_sensor(self):
        # Room 2 reports status notConnected and no value.
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getRoomHumidity("2")

    def test_getRoomCondensationRisk(self):
        self.assertFalse(self.device.getRoomCondensationRisk("0"))
        self.assertFalse(self.device.getRoomCondensationRisk("1"))
        self.assertFalse(self.device.getRoomCondensationRisk("2"))

    def test_getRoomSetpointComfortPerceived(self):
        self.assertAlmostEqual(self.device.getRoomSetpointComfortPerceived("0"), 22)
        self.assertAlmostEqual(self.device.getRoomSetpointComfortPerceived("1"), 22)
        self.assertAlmostEqual(self.device.getRoomSetpointComfortPerceived("2"), 22)

    def test_getRoomSetpointNormalPerceived(self):
        self.assertAlmostEqual(self.device.getRoomSetpointNormalPerceived("0"), 20.5)
        self.assertAlmostEqual(self.device.getRoomSetpointNormalPerceived("1"), 20)
        self.assertAlmostEqual(self.device.getRoomSetpointNormalPerceived("2"), 19)

    def test_getRoomChildLock(self):
        self.assertFalse(self.device.getRoomChildLockActive("0"))
        self.assertEqual(self.device.getRoomChildLockStatus("0"), "inactive")

    def test_getRoomHeatOnTimeEnabled(self):
        self.assertTrue(self.device.getRoomHeatOnTimeEnabled("0"))
        self.assertFalse(self.device.getRoomHeatOnTimeEnabled("1"))

    def test_getRoomHydraulicBalancingEnabled(self):
        self.assertTrue(self.device.getRoomHydraulicBalancingEnabled("0"))

    def test_getRoomOpenWindowDetectionEnabled(self):
        self.assertTrue(self.device.getRoomOpenWindowDetectionEnabled("0"))
        self.assertFalse(self.device.getRoomOpenWindowDetectionEnabled("2"))

    def test_getRoomWindowOpen(self):
        self.assertFalse(self.device.getRoomWindowOpen("0"))
        self.assertFalse(self.device.getRoomWindowOpen("1"))

    def test_getRoomWindowOpen_without_sensor(self):
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getRoomWindowOpen("2")

    def test_getRoomCO2_not_served(self):
        # This installation has no CO2 sensor in any room.
        for room_id in self.device.getAvailableRoomIds():
            with self.assertRaises(PyViCareNotSupportedFeatureError):
                self.device.getRoomCO2(room_id)

    def test_getRoomSetpointHeating(self):
        # Room 1 is in a reduced phase at 18; its normal level is 20.
        self.assertAlmostEqual(self.device.getRoomSetpointHeating("0"), 20.5)
        self.assertAlmostEqual(self.device.getRoomSetpointHeating("1"), 18)
        self.assertAlmostEqual(self.device.getRoomSetpointHeating("2"), 19)
