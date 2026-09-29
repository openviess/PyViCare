import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal200ASystemController(unittest.TestCase):

    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/Vitocal200A_SystemController.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_getAvailableCircuits(self):
        self.assertEqual(self.device.getAvailableCircuits(), ['0'])

    def test_getActiveMode(self):
        self.assertEqual(self.device.circuits[0].getActiveMode(), 'heating')

    def test_getActiveProgram(self):
        self.assertEqual(self.device.circuits[0].getActiveProgram(), 'normalHeating')

    def test_getSupplyTemperature(self):
        self.assertEqual(self.device.circuits[0].getSupplyTemperature(), 26.5)

    def test_getDomesticHotWaterStorageTemperature(self):
        self.assertEqual(self.device.getDomesticHotWaterStorageTemperature(), 51.4)

    def test_getDomesticHotWaterConfiguredTemperature(self):
        self.assertEqual(self.device.getDomesticHotWaterConfiguredTemperature(), 50)

    def test_getDomesticHotWaterActive(self):
        self.assertTrue(self.device.getDomesticHotWaterActive())

    def test_no_compressors_on_the_controller(self):
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getAvailableCompressors()


class Vitocal200AOutdoorUnit(unittest.TestCase):

    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "1")
        self.service = ViCareServiceMock('response/Vitocal200A_OutdoorUnit.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_getAvailableCompressors(self):
        self.assertEqual(self.device.getAvailableCompressors(), ['0'])

    def test_compressor_getActive(self):
        self.assertFalse(self.device.compressors[0].getActive())

    def test_compressor_getHours(self):
        self.assertEqual(self.device.compressors[0].getHours(), 1)

    def test_compressor_getStarts(self):
        self.assertEqual(self.device.compressors[0].getStarts(), 2)

    def test_getSupplyPressure(self):
        self.assertEqual(self.device.getSupplyPressure(), 1.2)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertEqual(self.device.getSupplyTemperaturePrimaryCircuit(), 20.6)

    def test_getSupplyTemperatureSecondaryCircuit(self):
        self.assertEqual(self.device.getSupplyTemperatureSecondaryCircuit(), 26.4)

    def test_no_circuits_on_the_outdoor_unit(self):
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.device.getAvailableCircuits()
