import unittest

from PyViCare.PyViCareElectricalEnergySystem import ElectricalEnergySystem
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class VitochargeEvolution08(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/VitochargeEvolution08.json')
        self.device = ElectricalEnergySystem(self.accessor, self.service)

    def test_getElectricalEnergySystemSOC(self):
        self.assertEqual(self.device.getElectricalEnergySystemSOC(), 43)

    def test_getElectricalEnergySystemOperationState(self):
        self.assertEqual(self.device.getElectricalEnergySystemOperationState(), "discharge")

    def test_getElectricalEnergySystemBatteryControlMode(self):
        self.assertEqual(self.device.getElectricalEnergySystemBatteryControlMode(), "nothing")

    def test_getElectricalEnergySystemBatteryControlModes(self):
        self.assertEqual(self.device.getElectricalEnergySystemBatteryControlModes(),
                         ["powerControlMode", "nothing", "pccControlMode"])

    def test_setElectricalEnergySystemBatteryControlMode(self):
        self.device.setElectricalEnergySystemBatteryControlMode("pccControlMode")
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'ess.battery.control.mode.active')
        self.assertEqual(
            self.service.setPropertyData[0]['action'], 'setMode')
        self.assertEqual(
            self.service.setPropertyData[0]['data'], {'value': 'pccControlMode'})
