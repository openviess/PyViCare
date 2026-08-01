import unittest

from PyViCare.PyViCareRoomControl import RoomControl
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class RoomControlTest(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/RoomControl.json')
        self.device = RoomControl(self.accessor, self.service)

    def test_getAvailableRoomIds(self):
        self.assertEqual(self.device.getAvailableRoomIds(), ["0", "1"])

    def test_getRoomTemperature(self):
        self.assertAlmostEqual(self.device.getRoomTemperature("0"), 23.4)
        self.assertAlmostEqual(self.device.getRoomTemperature("1"), 22.8)

    def test_getRoomHumidity(self):
        self.assertEqual(self.device.getRoomHumidity("0"), 49)
        self.assertEqual(self.device.getRoomHumidity("1"), 56)

    def test_getRoomCO2(self):
        self.assertEqual(self.device.getRoomCO2("0"), 1000)
        self.assertEqual(self.device.getRoomCO2("1"), 1000)

    def test_getRoomCondensationRisk(self):
        self.assertFalse(self.device.getRoomCondensationRisk("0"))
        self.assertFalse(self.device.getRoomCondensationRisk("1"))

    def test_getRoomSetpointComfortHeating(self):
        self.assertEqual(self.device.getRoomSetpointComfortHeating("0"), 20)
        self.assertEqual(self.device.getRoomSetpointComfortHeating("1"), 23)

    def test_getRoomSetpointNormalHeating(self):
        self.assertEqual(self.device.getRoomSetpointNormalHeating("0"), 18)
        self.assertEqual(self.device.getRoomSetpointNormalHeating("1"), 22)

    def test_getRoomSetpointReducedHeating(self):
        self.assertEqual(self.device.getRoomSetpointReducedHeating("0"), 16)
        self.assertEqual(self.device.getRoomSetpointReducedHeating("1"), 21)

    def test_getRoomSetpointNormalPerceived(self):
        self.assertEqual(self.device.getRoomSetpointNormalPerceived("0"), 18)
        self.assertEqual(self.device.getRoomSetpointNormalPerceived("1"), 22)

    def test_getRoomSetpointComfortPerceived(self):
        self.assertEqual(self.device.getRoomSetpointComfortPerceived("0"), 20)
        self.assertEqual(self.device.getRoomSetpointComfortPerceived("1"), 23)

    def test_getRoomSetpointCoolingNotSupportedWhenDisabled(self):
        # Cooling levels exist on the API but return no value on this scope
        # for heating-only rooms; the getter surfaces that as NotSupported.
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getRoomSetpointNormalCooling("0")

    def test_getRoomChildLockActive(self):
        self.assertFalse(self.device.getRoomChildLockActive("0"))
        self.assertFalse(self.device.getRoomChildLockActive("1"))

    def test_getRoomChildLockStatus(self):
        self.assertEqual(self.device.getRoomChildLockStatus("0"), "inactive")
        self.assertEqual(self.device.getRoomChildLockStatus("1"), "inactive")

    def test_getRoomWindowOpen(self):
        self.assertFalse(self.device.getRoomWindowOpen("0"))
        self.assertFalse(self.device.getRoomWindowOpen("1"))

    def test_getRoomOpenWindowDetectionEnabled(self):
        self.assertFalse(self.device.getRoomOpenWindowDetectionEnabled("0"))
        self.assertTrue(self.device.getRoomOpenWindowDetectionEnabled("1"))

    def test_getRoomHydraulicBalancingEnabled(self):
        self.assertTrue(self.device.getRoomHydraulicBalancingEnabled("0"))
        self.assertTrue(self.device.getRoomHydraulicBalancingEnabled("1"))

    def test_getRoomTrvAlgorithmEnabled(self):
        self.assertFalse(self.device.getRoomTrvAlgorithmEnabled("0"))
        self.assertFalse(self.device.getRoomTrvAlgorithmEnabled("1"))

    def test_getRoomHeatOnTimeEnabled(self):
        self.assertTrue(self.device.getRoomHeatOnTimeEnabled("0"))
        self.assertFalse(self.device.getRoomHeatOnTimeEnabled("1"))
