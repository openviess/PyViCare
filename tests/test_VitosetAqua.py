import unittest

from PyViCare.PyViCareWaterTreatment import WaterTreatment
from tests.ViCareServiceMock import ViCareServiceMock


class VitosetAquaTest(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/VitosetAqua.json')
        self.device = WaterTreatment(self.service)

    # --- Softener ---

    def test_getSaltDaysRemaining(self):
        self.assertEqual(self.device.getSaltDaysRemaining(), 15)

    def test_getLowSaltAlertDays(self):
        self.assertEqual(self.device.getLowSaltAlertDays(), 14)

    # --- Consumption ---

    def test_getCurrentFlow(self):
        self.assertEqual(self.device.getCurrentFlow(), 0.0)

    def test_getMaxFlow(self):
        self.assertAlmostEqual(self.device.getMaxFlow(), 40.2)

    def test_getCurrentDayConsumption(self):
        self.assertEqual(self.device.getCurrentDayConsumption(), 144)

    def test_getLastSevenDaysConsumption(self):
        self.assertEqual(self.device.getLastSevenDaysConsumption(), 201)

    def test_getTotalConsumption(self):
        self.assertEqual(self.device.getTotalConsumption(), 45510)

    # --- Leak Detection ---

    def test_getLeakSensors_returns_only_connected(self):
        sensors = self.device.getLeakSensors()
        self.assertEqual(len(sensors), 1)

    def test_getLeakSensors_first_sensor_fields(self):
        sensor = self.device.getLeakSensors()[0]
        self.assertEqual(sensor["slot"], 0)
        self.assertEqual(sensor["status"], "connected")
        self.assertFalse(sensor["leak_detected"])
        self.assertEqual(sensor["id"], "00:00:00:00:00:00:00:00")
        self.assertEqual(sensor["name"], "Basement")
        self.assertEqual(sensor["battery_percent"], 100)
        self.assertEqual(sensor["rssi_dbm"], 0)
        self.assertIsInstance(sensor["hardware_version"], dict)
        self.assertIsInstance(sensor["software_version"], dict)
        for field in ("build", "family", "revision", "version"):
            self.assertIn(field, sensor["hardware_version"])
            self.assertIn(field, sensor["software_version"])

    def test_getFlowAlertMaxDuration(self):
        self.assertEqual(self.device.getFlowAlertMaxDuration(), 0)

    def test_getFlowAlertMaxFlow(self):
        self.assertEqual(self.device.getFlowAlertMaxFlow(), 0.0)

    # --- Shutoff Valve ---

    def test_getShutoffPosition(self):
        self.assertEqual(self.device.getShutoffPosition(), "open")

    def test_getShutoffMotorState(self):
        self.assertEqual(self.device.getShutoffMotorState(), "off")

    def test_getHolidayModeActive(self):
        self.assertFalse(self.device.getHolidayModeActive())

    # --- Inherited from Device ---

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), "################")


if __name__ == '__main__':
    unittest.main()
