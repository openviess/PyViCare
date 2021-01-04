import unittest
from tests.ViCareServiceForTesting import ViCareServiceForTesting
from PyViCare.PyViCareDevice import Device

class GenericDevice(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceForTesting(None, 0, {})
        self.device = Device(None, None, None, 0, 0, self.service)
        
    def test_activateComfort(self):
        self.device.activateComfort()
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'activate')
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'heating.circuits.0.operating.programs.comfort')

    def test_deactivateComfort(self):
        self.device.deactivateComfort()
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'deactivate')
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'heating.circuits.0.operating.programs.comfort')

    def test_setDomesticHotWaterTemperature(self):
        self.device.setDomesticHotWaterTemperature(50)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'heating.dhw.temperature')
        self.assertEqual(self.service.setPropertyData[0]['action'], 'setTargetTemperature')
        self.assertEqual(self.service.setPropertyData[0]['data'], '{"temperature":50}')

    def test_setMode(self):
        self.device.setMode('dhw')
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['property_name'], 'heating.circuits.0.operating.modes.active')
        self.assertEqual(self.service.setPropertyData[0]['action'], 'setMode')
        self.assertEqual(self.service.setPropertyData[0]['data'], '{"mode":"dhw"}')

    