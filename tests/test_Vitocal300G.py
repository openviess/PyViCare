import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal300G(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal300G_CU401B.json')
        self.device = HeatPump(self.service)

    # COP (Coefficient of Performance) tests
    def test_getCoefficientOfPerformanceHeating(self):
        self.assertAlmostEqual(
            self.device.getCoefficientOfPerformanceHeating(), 4.8)

    def test_getCoefficientOfPerformanceDHW(self):
        self.assertAlmostEqual(
            self.device.getCoefficientOfPerformanceDHW(), 4.0)

    def test_getCoefficientOfPerformanceTotal(self):
        self.assertAlmostEqual(
            self.device.getCoefficientOfPerformanceTotal(), 4.7)

    def test_getCoefficientOfPerformanceCooling(self):
        self.assertAlmostEqual(
            self.device.getCoefficientOfPerformanceCooling(), 0.0)

    # Compressor power tests
    def test_compressor_getPower(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getPower(), 12.0)

    def test_compressor_getPowerUnit(self):
        self.assertEqual(
            self.device.compressors[0].getPowerUnit(), "kilowatt")

    def test_compressor_getModulation(self):
        self.assertEqual(
            self.device.compressors[0].getModulation(), 100)

    def test_compressor_getModulationUnit(self):
        self.assertEqual(
            self.device.compressors[0].getModulationUnit(), "percent")

    # Compressor statistics tests
    def test_compressor_getActive(self):
        self.assertEqual(self.device.compressors[0].getActive(), True)

    def test_compressor_getPhase(self):
        self.assertEqual(self.device.compressors[0].getPhase(), "heating")

    def test_compressor_getHours(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHours(), 942.4)

    def test_compressor_getStarts(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getStarts(), 363)

    # Load class tests - use statistics.load fallback path
    def test_compressor_getHoursLoadClass1(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass1(), 5)

    def test_compressor_getHoursLoadClass2(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass2(), 233)

    def test_compressor_getHoursLoadClass3(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass3(), 448)

    def test_compressor_getHoursLoadClass4(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass4(), 249)

    def test_compressor_getHoursLoadClass5(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getHoursLoadClass5(), 3)

    # Compressor sensor tests
    def test_compressor_getInletPressure(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getInletPressure(), 8.7)

    def test_compressor_getInletTemperature(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getInletTemperature(), 7.1)

    def test_compressor_getOutletTemperature(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getOutletTemperature(), 79.5)

    def test_compressor_getOverheatTemperature(self):
        self.assertAlmostEqual(
            self.device.compressors[0].getOverheatTemperature(), 4.0)

    # General device tests
    def test_getOutsideTemperature(self):
        self.assertAlmostEqual(
            self.device.getOutsideTemperature(), 4.1)

    def test_getReturnTemperature(self):
        self.assertAlmostEqual(self.device.getReturnTemperature(), 35.8)

    def test_getSupplyTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(
            self.device.getSupplyTemperaturePrimaryCircuit(), 8.7)

    def test_getReturnTemperaturePrimaryCircuit(self):
        self.assertAlmostEqual(self.device.getReturnTemperaturePrimaryCircuit(), 4.9)

    # DHW tests
    def test_getDomesticHotWaterStorageTemperature(self):
        self.assertAlmostEqual(
            self.device.getDomesticHotWaterStorageTemperature(), 52.4)

    def test_getDomesticHotWaterConfiguredTemperature(self):
        self.assertAlmostEqual(
            self.device.getDomesticHotWaterConfiguredTemperature(), 50.0)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), False)

    def test_getHotWaterStorageTemperatureTop(self):
        self.assertAlmostEqual(
            self.device.getHotWaterStorageTemperatureTop(), 52.4)

    # Buffer tests
    def test_getBufferMainTemperature(self):
        self.assertAlmostEqual(
            self.device.getBufferMainTemperature(), 36.2)

    def test_getBufferTopTemperature(self):
        self.assertAlmostEqual(
            self.device.getBufferTopTemperature(), 36.2)

    # Circuit tests
    def test_circuit_getSupplyTemperature(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getSupplyTemperature(), 36.1)

    def test_getHeatingCurveSlope(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveSlope(), 1.0)

    def test_getHeatingCurveShift(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getHeatingCurveShift(), 2)

    def test_circuit_getActiveMode(self):
        self.assertEqual(
            self.device.circuits[0].getActiveMode(), "dhwAndHeating")

    def test_circuit_getActiveProgram(self):
        self.assertEqual(
            self.device.circuits[0].getActiveProgram(), "normal")

    def test_circuit_getTargetTemperature(self):
        self.assertAlmostEqual(
            self.device.circuits[0].getTargetTemperature(), 40)

    def test_getPrograms(self):
        expected_programs = ['comfort', 'eco', 'fixed', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['dhw', 'dhwAndHeating', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getModes(), expected_modes)

    # Primary circuit pump tests
    def test_getPrimaryCircuitPumpRotation(self):
        self.assertAlmostEqual(
            self.device.getPrimaryCircuitPumpRotation(), 80)

    def test_getPrimaryCircuitPumpRotationUnit(self):
        self.assertEqual(
            self.device.getPrimaryCircuitPumpRotationUnit(), "percent")

    # Pressure sensor tests (refrigerant circuit)
    def test_getHotGasPressure(self):
        self.assertAlmostEqual(
            self.device.getHotGasPressure(), 28.1)

    def test_getHotGasPressureUnit(self):
        self.assertEqual(
            self.device.getHotGasPressureUnit(), "bar")

    def test_getSuctionGasPressure(self):
        self.assertAlmostEqual(
            self.device.getSuctionGasPressure(), 8.7)

    def test_getSuctionGasPressureUnit(self):
        self.assertEqual(
            self.device.getSuctionGasPressureUnit(), "bar")

    # Temperature sensor tests (refrigerant circuit)
    def test_getHotGasTemperature(self):
        self.assertAlmostEqual(
            self.device.getHotGasTemperature(), 79.5)

    def test_getLiquidGasTemperature(self):
        self.assertAlmostEqual(
            self.device.getLiquidGasTemperature(), 36)

    def test_getSuctionGasTemperature(self):
        self.assertAlmostEqual(
            self.device.getSuctionGasTemperature(), 7.1)

    # Main ECU runtime test
    def test_getMainECURuntime(self):
        self.assertEqual(
            self.device.getMainECURuntime(), 7768472)

    def test_getMainECURuntimeUnit(self):
        self.assertEqual(
            self.device.getMainECURuntimeUnit(), "seconds")

    # Heating rod runtime tests
    def test_getHeatingRodRuntimeLevelOne(self):
        self.assertEqual(
            self.device.getHeatingRodRuntimeLevelOne(), 886682)

    def test_getHeatingRodRuntimeLevelTwo(self):
        self.assertEqual(
            self.device.getHeatingRodRuntimeLevelTwo(), 287877)

    # Configuration tests
    def test_getConfigurationBufferTemperatureMax(self):
        self.assertAlmostEqual(
            self.device.getConfigurationBufferTemperatureMax(), 65)

    def test_getConfigurationOutsideTemperatureDampingFactor(self):
        self.assertEqual(
            self.device.getConfigurationOutsideTemperatureDampingFactor(), 180)

    def test_getConfigurationHeatingRodDHWApproved(self):
        self.assertEqual(
            self.device.getConfigurationHeatingRodDHWApproved(), False)

    def test_getConfigurationHeatingRodHeatingApproved(self):
        self.assertEqual(
            self.device.getConfigurationHeatingRodHeatingApproved(), False)

    def test_getConfigurationDHWHeaterApproved(self):
        self.assertEqual(
            self.device.getConfigurationDHWHeaterApproved(), True)

    # Cooling circuit tests
    def test_getAvailableCoolingCircuits(self):
        self.assertEqual(
            self.device.getAvailableCoolingCircuits(), ['0'])

    def test_coolingCircuit_getType(self):
        self.assertEqual(
            self.device.coolingCircuits[0].getType(), "VC 3xx-G Emerson")

    def test_coolingCircuit_getReverseActive(self):
        self.assertEqual(
            self.device.coolingCircuits[0].getReverseActive(), False)

    def test_getHeatingScheduleModes(self):
        expected_modes = {'reduced', 'normal', 'fixed'}
        self.assertSetEqual(
            set(self.device.circuits[0].getHeatingScheduleModes()), expected_modes)
