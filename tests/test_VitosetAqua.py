import unittest

from PyViCare.PyViCareWaterTreatment import LeakSensor, WaterTreatment
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

    def test_getTotalConsumption(self):
        self.assertEqual(self.device.getTotalConsumption(), 45510)

    # --- Leak Detection ---

    def test_leakSensors_returns_only_connected(self):
        self.assertEqual(len(self.device.leakSensors), 1)

    def test_getAvailableLeakSensorSlots(self):
        self.assertEqual(self.device.getAvailableLeakSensorSlots(), [0])

    def test_leakSensor_fields(self):
        sensor = self.device.leakSensors[0]
        self.assertIsInstance(sensor, LeakSensor)
        self.assertEqual(sensor.slot, 0)
        self.assertEqual(sensor.id, 0)
        self.assertEqual(sensor.getStatus(), "connected")
        self.assertFalse(sensor.getLeakDetected())
        self.assertEqual(sensor.getSensorId(), "00:00:00:00:00:00:00:00")
        self.assertEqual(sensor.getName(), "Basement")
        self.assertEqual(sensor.getBatteryPercent(), 100)
        self.assertEqual(sensor.getRssi(), 0)
        for field in ("build", "family", "revision", "version"):
            self.assertIn(field, sensor.getHardwareVersion())
            self.assertIn(field, sensor.getSoftwareVersion())

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
