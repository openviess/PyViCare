import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.helper import now_is
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens200W_2(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/Vitodens200W_2.json')
        self.device = GazBoiler(self.accessor, self.service)

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), '################')

    def test_getActive(self):
        self.assertEqual(self.device.burners[0].getActive(), False)

    def test_getDomesticHotWaterActive(self):
        self.assertEqual(self.device.getDomesticHotWaterActive(), True)

    def test_getBurnerStarts(self):
        self.assertEqual(self.device.burners[0].getStarts(), 41460)

    def test_getBurnerHours(self):
        self.assertEqual(self.device.burners[0].getHours(), 19016.7)

    def test_getBurnerModulation(self):
        self.assertEqual(self.device.burners[0].getModulation(), 0)

    def test_getPrograms(self):
        expected_programs = ['comfort', 'eco', 'external', 'holiday', 'normal', 'reduced', 'standby']
        self.assertListEqual(
            self.device.circuits[0].getPrograms(), expected_programs)

    def test_getModes(self):
        expected_modes = ['standby', 'dhw', 'dhwAndHeating', 'forcedReduced', 'forcedNormal']
        self.assertListEqual(
            self.device.circuits[0].getModes(), expected_modes)

    def test_getPowerConsumptionDays(self):
        expected_days = [0.283, 0.269, 0.272, 0.279, 0.287, 0.271, 0.273, 0.269]
        self.assertEqual(self.device.getPowerConsumptionDays(), expected_days)

    def test_getDomesticHotWaterMaxTemperature(self):
        self.assertEqual(self.device.getDomesticHotWaterMaxTemperature(), 60)

    def test_getDomesticHotWaterMinTemperature(self):
        self.assertEqual(self.device.getDomesticHotWaterMinTemperature(), 10)

    def test_getFrostProtectionActive(self):
        self.assertEqual(
            self.device.circuits[0].getFrostProtectionActive(), False)

    def test_getDomesticHotWaterCirculationPumpActive(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationPumpActive(), True)

    def test_getDomesticHotWaterConfiguredTemperature(self):
        self.assertEqual(
            self.device.getDomesticHotWaterConfiguredTemperature(), 55)

    def test_getDomesticHotWaterCirculationScheduleModes(self):
        self.assertEqual(
            self.device.getDomesticHotWaterCirculationScheduleModes(), ['on'])

    def test_getDomesticHotWaterCirculationMode_wed_07_30_time(self):
        with now_is('2021-09-08 07:30:00'):
            self.assertEqual(
                self.device.getDomesticHotWaterCirculationMode(), 'on')

    def test_getDomesticHotWaterCirculationMode_wed_10_10_time(self):
        with now_is('2021-09-08 10:10:00'):
            self.assertEqual(
                self.device.getDomesticHotWaterCirculationMode(), 'on')

    def test_getGasConsumptionHeatingUnit(self):
        self.assertEqual(
            self.device.getGasConsumptionHeatingUnit(), "kilowattHour")

    def test_getGasConsumptionHeatingToday(self):
        self.assertEqual(
            self.device.getGasConsumptionHeatingToday(), 0)

    def test_getGasConsumptionDomesticHotWaterUnit(self):
        self.assertEqual(
            self.device.getGasConsumptionDomesticHotWaterUnit(), "kilowattHour")

    def test_getGasConsumptionDomesticHotWaterToday(self):
        self.assertEqual(
            self.device.getGasConsumptionDomesticHotWaterToday(), 29)

    def test_getPowerConsumptionUnit(self):
        self.assertEqual(
            self.device.getPowerConsumptionUnit(), "kilowattHour")

    def test_getPowerConsumptionToday(self):
        self.assertEqual(
            self.device.getPowerConsumptionToday(), 0.283)

    def test_getActiveProgram(self):
        self.assertEqual(self.device.circuits[0].getActiveProgram(), 'standby')

    def test_getProgramTemperatures(self):
        self.assertEqual(self.device.circuits[0].getReducedTemperature(), 17)
        self.assertEqual(self.device.circuits[0].getComfortTemperature(), 22)
        self.assertEqual(self.device.circuits[0].getNormalTemperature(), 21)

        # active program is 'standby', so there's no active temperature
        self.assertIsNone(self.device.circuits[0].getActiveProgramTemperature())

    def test_setProgramTemperatures(self):
        self.device.circuits[0].setReducedTemperature(18)
        self.device.circuits[0].setComfortTemperature(23)
        self.device.circuits[0].setNormalTemperature(22)

        self.assertEqual(len(self.service.setPropertyData), 3)

        for i, program, temperature in [(0, 'reduced', 18), (1, 'comfort', 23), (2, 'normal', 22)]:
            self.assertEqual(
                self.service.setPropertyData[i]['property_name'],
                f'heating.circuits.0.operating.programs.{program}'
            )
            self.assertEqual(
                self.service.setPropertyData[i]['action'],
                'setTemperature'
            )
            self.assertEqual(
                self.service.setPropertyData[i]['data'],
                {'targetTemperature': temperature}
            )

    def test_activateComfort(self):
        self.device.circuits[0].activateComfort()

        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'],
            'heating.circuits.0.operating.programs.comfort'
        )
        self.assertEqual(
            self.service.setPropertyData[0]['action'],
            'activate'
        )
        self.assertEqual(self.service.setPropertyData[0]['data'], {})

    def test_deactivateComfort(self):
        self.device.circuits[0].deactivateComfort()

        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'],
            'heating.circuits.0.operating.programs.comfort'
        )
        self.assertEqual(
            self.service.setPropertyData[0]['action'],
            'deactivate'
        )
        self.assertEqual(self.service.setPropertyData[0]['data'], {})
