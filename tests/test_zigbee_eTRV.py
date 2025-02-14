import unittest

from PyViCare.PyViCareRadiatorActuator import RadiatorActuator
from tests.ViCareServiceMock import ViCareServiceMock


class ZK03840(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/zigbee_Smart_Device_eTRV_generic_50.json')
        self.device = RadiatorActuator(self.service)

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), "zigbee-048727fffeb429ae")

    def test_isDomesticHotWaterDevice(self):
        self.assertEqual(self.device.isDomesticHotWaterDevice(), False)

    def test_isSolarThermalDevice(self):
        self.assertEqual(self.device.isSolarThermalDevice(), False)

    def test_isVentilationDevice(self):
        self.assertEqual(self.device.isVentilationDevice(), False)

    def test_getTemperature(self):
        self.assertEqual(self.device.getTemperature(), 16.5)

    def test_getBatteryLevel(self):
        self.assertEqual(self.device.getBatteryLevel(), 66)

    def test_getTargetTemperature(self):
        self.assertEqual(self.device.getTargetTemperature(), 8)

    def test_setTargetTemperature(self):
        self.device.setTargetTemperature(22)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'trv.temperature')
        self.assertEqual(self.service.setPropertyData[0]['action'], 'setTargetTemperature')
        self.assertEqual(self.service.setPropertyData[0]['data'], {'temperature': 22})
