import unittest

from PyViCare.PyViCareRepeater import Repeater
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class ZK05390ViaHeatbox2(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "zigbee-################")
        self.service = ViCareServiceMock('response/zigbee_zk05390_repeater.json')
        self.device = Repeater(self.accessor, self.service)

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
            self.device.getZigbeeParentID(), "################")
