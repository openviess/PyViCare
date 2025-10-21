import unittest

from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareRadiatorActuator import RadiatorActuator
from tests.ViCareServiceMock import ViCareServiceMock


class ZK03840ViaHeatbox2(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "[device]")
        self.service = ViCareServiceMock('response/zigbee_zk03840_trv.json')
        self.device = RadiatorActuator(self.accessor, self.service)

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), "zigbee-################")

    def test_isDomesticHotWaterDevice(self):
        self.assertEqual(self.device.isDomesticHotWaterDevice(), False)

    def test_isSolarThermalDevice(self):
        self.assertEqual(self.device.isSolarThermalDevice(), False)

    def test_isVentilationDevice(self):
        self.assertEqual(self.device.isVentilationDevice(), False)

    def test_getTemperature(self):
        self.assertEqual(
            self.device.getTemperature(), 21.5)

    def test_getTargetTemperature(self):
        self.assertEqual(
            self.device.getTargetTemperature(), 21.5)

    def test_setTargetTemperature(self):
        self.device.setTargetTemperature(22)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'trv.temperature')
        self.assertEqual(self.service.setPropertyData[0]['action'], 'setTargetTemperature')
        self.assertEqual(self.service.setPropertyData[0]['data'], {'temperature': 22})

    def test_isValveOpen(self):
        self.assertTrue(self.device.isValveOpen())
