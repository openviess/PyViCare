import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal250ATwoCircuits(unittest.TestCase):
    """Vitocal 250-A with two active heating circuits (radiators + underfloor heating)."""

    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/Vitocal250A_TwoCircuits.json')
        self.device = HeatPump(self.accessor, self.service)

    def test_circuits(self):
        self.assertEqual([circuit.circuit for circuit in self.device.circuits], ['0', '1'])

    def test_circuit_getName(self):
        self.assertEqual(self.device.circuits[0].getName(), "Heizkörper")
        self.assertEqual(self.device.circuits[1].getName(), "Fußbodenheizung")

    def test_circuit_getActive(self):
        self.assertTrue(self.device.circuits[0].getActive())
        self.assertTrue(self.device.circuits[1].getActive())

    def test_circuit_getType(self):
        self.assertEqual(self.device.circuits[0].getType(), "heatingCircuit")
        self.assertEqual(self.device.circuits[1].getType(), "heatingCircuit")

    def test_circuit_getHeatingCurveSlope(self):
        self.assertEqual(self.device.circuits[0].getHeatingCurveSlope(), 0.6)
        self.assertEqual(self.device.circuits[1].getHeatingCurveSlope(), 0.3)

    def test_circuit_getHeatingCurveShift(self):
        self.assertEqual(self.device.circuits[0].getHeatingCurveShift(), 0)
        self.assertEqual(self.device.circuits[1].getHeatingCurveShift(), 0)

    def test_circuit_getSupplyTemperature(self):
        self.assertEqual(self.device.circuits[0].getSupplyTemperature(), 22.1)
        self.assertEqual(self.device.circuits[1].getSupplyTemperature(), 22.3)

    def test_circuit_getModes(self):
        for circuit in self.device.circuits:
            self.assertEqual(circuit.getModes(), ['heating', 'standby'])
            self.assertEqual(circuit.getActiveMode(), 'heating')

    def test_circuit_getActiveProgram(self):
        self.assertEqual(self.device.circuits[0].getActiveProgram(), 'normalHeating')
        self.assertEqual(self.device.circuits[1].getActiveProgram(), 'normalHeating')

    def test_circuit_getDesiredTemperatureForProgram(self):
        radiators, underfloor = self.device.circuits
        self.assertEqual(radiators.getDesiredTemperatureForProgram('comfortHeating'), 22)
        self.assertEqual(radiators.getDesiredTemperatureForProgram('normalHeating'), 19)
        self.assertEqual(radiators.getDesiredTemperatureForProgram('reducedHeating'), 18)
        self.assertEqual(underfloor.getDesiredTemperatureForProgram('comfortHeating'), 22)
        self.assertEqual(underfloor.getDesiredTemperatureForProgram('normalHeating'), 20)
        self.assertEqual(underfloor.getDesiredTemperatureForProgram('reducedHeating'), 17)

    def test_circuit_getFrostProtectionActive(self):
        self.assertFalse(self.device.circuits[0].getFrostProtectionActive())
        self.assertFalse(self.device.circuits[1].getFrostProtectionActive())

    def test_circuit_getCirculationPumpActive(self):
        self.assertTrue(self.device.circuits[0].getCirculationPumpActive())
        self.assertTrue(self.device.circuits[1].getCirculationPumpActive())

    def test_compressor(self):
        compressor = self.device.compressors[0]
        self.assertFalse(compressor.getActive())
        self.assertEqual(compressor.getPhase(), "ready")
        self.assertEqual(compressor.getHours(), 31)
        self.assertEqual(compressor.getStarts(), 76)

    def test_getTemperatures(self):
        self.assertEqual(self.device.getOutsideTemperature(), 16)
        self.assertEqual(self.device.getReturnTemperature(), 27.8)
        self.assertEqual(self.device.getBufferMainTemperature(), 22.1)
        self.assertEqual(self.device.getSupplyTemperaturePrimaryCircuit(), 16.9)
        self.assertEqual(self.device.getDomesticHotWaterStorageTemperature(), 54.8)

    def test_getSupplyPressure(self):
        self.assertEqual(self.device.getSupplyPressure(), 1.5)

    def test_getDomesticHotWaterActiveOperatingMode(self):
        self.assertEqual(self.device.getDomesticHotWaterActiveOperatingMode(), 'efficientWithMinComfort')

    def test_getPowerSummaryConsumption(self):
        self.assertEqual(self.device.getPowerSummaryConsumptionHeatingCurrentYear(), 8.5)
        self.assertAlmostEqual(self.device.getPowerSummaryConsumptionDomesticHotWaterCurrentYear(), 58.3)

    def test_getHeatingRod(self):
        self.assertEqual(self.device.getHeatingRodStarts(), 1)
        self.assertEqual(self.device.getHeatingRodHours(), 0)

    def test_inverter(self):
        inverter = self.device.inverters[0]
        self.assertEqual(inverter.getPower(), 0.0)
        self.assertEqual(inverter.getCurrent(), 0.0)
        self.assertEqual(inverter.getTemperature(), 27.6)

    def test_getWifiSignalStrength(self):
        self.assertEqual(self.device.getWifiSignalStrength(), -63)
