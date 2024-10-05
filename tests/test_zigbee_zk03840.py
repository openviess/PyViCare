import unittest

from PyViCare.PyViCareRadiatorActuator import RadiatorActuator
from tests.ViCareServiceMock import ViCareServiceMock


class ZK03840(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/zigbee_zk03840_trv.json')
        self.device = RadiatorActuator(self.service)

    def test_isHeatingDevice(self):
        self.assertFalse(self.device.isHeatingDevice())

    def test_isDomesticHotWaterDevice(self):
        self.assertFalse(self.device.isDomesticHotWaterDevice())

    def test_isSolarThermalDevice(self):
        self.assertFalse(self.device.isSolarThermalDevice())

    def test_isVentilationDevice(self):
        self.assertFalse(self.device.isVentilationDevice())

    def test_getTemperature(self):
        self.assertEqual(
            self.device.getTemperature(), 18.4)

    def test_getTargetTemperature(self):
        self.assertEqual(
            self.device.getTargetTemperature(), 8)

    def test_setTargetTemperature(self):
        self.device.setTargetTemperature(22)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'trv.temperature')
        self.assertEqual(
            self.service.setPropertyData[0]['action'], 'setTargetTemperature')
        self.assertEqual(self.service.setPropertyData[0]['data'], {
                         'temperature': 22})
