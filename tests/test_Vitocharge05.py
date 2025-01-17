import unittest

from PyViCare.PyViCareElectricalEnergySystem import ElectricalEnergySystem
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocharge05(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocharge05.json')
        self.device = ElectricalEnergySystem(self.service)

    def test_isDomesticHotWaterDevice(self):
        self.assertEqual(self.device.isDomesticHotWaterDevice(), False)

    def test_isSolarThermalDevice(self):
        self.assertEqual(self.device.isSolarThermalDevice(), False)

    def test_isVentilationDevice(self):
        self.assertEqual(self.device.isVentilationDevice(), False)

    def test_getSerial(self):
        self.assertEqual(self.device.getSerial(), '################')

    def test_getPointOfCommonCouplingTransferPowerExchange(self):
        self.assertEqual(self.device.getPointOfCommonCouplingTransferPowerExchange(), 6624)

    def test_getPhotovoltaicProductionCumulatedUnit(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedUnit(), "wattHour")

    def test_getPhotovoltaicProductionCumulatedCurrentDay(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedCurrentDay(), 4534)

    def test_getPhotovoltaicProductionCumulatedCurrentWeek(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedCurrentWeek(), 12483)

    def test_getPhotovoltaicProductionCumulatedCurrentMonth(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedCurrentMonth(), 23498)

    def test_getPhotovoltaicProductionCumulatedCurrentYear(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedCurrentYear(), 23498)

    def test_getPhotovoltaicProductionCumulatedLifeCycle(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedLifeCycle(), 23498)

    def test_getPhotovoltaicStatus(self):
        self.assertEqual(self.device.getPhotovoltaicStatus(), "ready")

    def test_getPhotovoltaicProductionCurrent(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCurrent(), 0)

    def test_getPhotovoltaicProductionCurrentUnit(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCurrentUnit(), "kilowatt")

    def test_getPointOfCommonCouplingTransferConsumptionTotal(self):
        self.assertEqual(self.device.getPointOfCommonCouplingTransferConsumptionTotal(), 3258900)

    def test_getPointOfCommonCouplingTransferConsumptionTotalUnit(self):
        self.assertEqual(self.device.getPointOfCommonCouplingTransferConsumptionTotalUnit(), "wattHour")

    def test_getPointOfCommonCouplingTransferFeedInTotal(self):
        self.assertEqual(self.device.getPointOfCommonCouplingTransferFeedInTotal(), 29200)

    def test_getPointOfCommonCouplingTransferFeedInTotalUnit(self):
        self.assertEqual(self.device.getPointOfCommonCouplingTransferFeedInTotalUnit(), "wattHour")

    def test_getElectricalEnergySystemTransferDischargeCumulatedUnit(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedUnit(), "wattHour")

    def test_getElectricalEnergySystemTransferDischargeCumulatedCurrentDay(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedCurrentDay(), 1245)

    def test_getElectricalEnergySystemTransferDischargeCumulatedCurrentWeek(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedCurrentWeek(), 3232)

    def test_getElectricalEnergySystemTransferDischargeCumulatedCurrentMonth(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedCurrentMonth(), 3982)

    def test_getElectricalEnergySystemTransferDischargeCumulatedCurrentYear(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedCurrentYear(), 3982)

    def test_getElectricalEnergySystemTransferDischargeCumulatedLifeCycle(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedLifeCycle(), 3982)

    def test_getElectricalEnergySystemSOC(self):
        self.assertEqual(self.device.getElectricalEnergySystemSOC(), 0)

    def test_getElectricalEnergySystemSOCUnit(self):
        self.assertEqual(self.device.getElectricalEnergySystemSOCUnit(), "percent")

    def test_getElectricalEnergySystemPower(self):
        self.assertEqual(self.device.getElectricalEnergySystemPower(), 0)

    def test_getElectricalEnergySystemPowerUnit(self):
        self.assertEqual(self.device.getElectricalEnergySystemPowerUnit(), "watt")

    def test_getElectricalEnergySystemOperationState(self):
        self.assertEqual(self.device.getElectricalEnergySystemOperationState(), "standby")
