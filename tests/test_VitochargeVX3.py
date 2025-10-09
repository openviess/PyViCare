import unittest

from PyViCare.PyViCareElectricalEnergySystem import ElectricalEnergySystem
from tests.ViCareServiceMock import ViCareServiceMock

ROLES = [
    "capability:hems",
    "type:E3",
    "type:ess",
    "type:photovoltaic;Internal",
    "type:product;Vitocharge"
]

class VitochargeVX3(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock(ROLES, 'response/VitochargeVX3.json')
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
        self.assertEqual(self.device.getPointOfCommonCouplingTransferPowerExchange(), 4)

    def test_getPhotovoltaicProductionCumulatedUnit(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedUnit(), "wattHour")

    def test_getPhotovoltaicProductionCumulatedCurrentDay(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedCurrentDay(), 30077)

    def test_getPhotovoltaicProductionCumulatedCurrentWeek(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedCurrentWeek(), 30078)

    def test_getPhotovoltaicProductionCumulatedCurrentMonth(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedCurrentMonth(), 927873)

    def test_getPhotovoltaicProductionCumulatedCurrentYear(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedCurrentYear(), 10732404)

    def test_getPhotovoltaicProductionCumulatedLifeCycle(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCumulatedLifeCycle(), 15510008)

    def test_getPhotovoltaicStatus(self):
        self.assertEqual(self.device.getPhotovoltaicStatus(), "ready")

    def test_getPhotovoltaicProductionCurrent(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCurrent(), 0)

    def test_getPhotovoltaicProductionCurrentUnit(self):
        self.assertEqual(self.device.getPhotovoltaicProductionCurrentUnit(), "kilowatt")

    def test_getPointOfCommonCouplingTransferConsumptionTotal(self):
        self.assertEqual(self.device.getPointOfCommonCouplingTransferConsumptionTotal(), 2844400)

    def test_getPointOfCommonCouplingTransferConsumptionTotalUnit(self):
        self.assertEqual(self.device.getPointOfCommonCouplingTransferConsumptionTotalUnit(), "wattHour")

    def test_getPointOfCommonCouplingTransferFeedInTotal(self):
        self.assertEqual(self.device.getPointOfCommonCouplingTransferFeedInTotal(), 10433300)

    def test_getPointOfCommonCouplingTransferFeedInTotalUnit(self):
        self.assertEqual(self.device.getPointOfCommonCouplingTransferFeedInTotalUnit(), "wattHour")

    def test_getElectricalEnergySystemTransferChargeCumulatedUnit(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferChargeCumulatedUnit(), "wattHour")

    def test_getElectricalEnergySystemTransferChargeCumulatedCurrentDay(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferChargeCumulatedCurrentDay(), 5449)

    def test_getElectricalEnergySystemTransferChargeCumulatedCurrentWeek(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferChargeCumulatedCurrentWeek(), 5450)

    def test_getElectricalEnergySystemTransferChargeCumulatedCurrentMonth(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferChargeCumulatedCurrentMonth(), 143145)

    def test_getElectricalEnergySystemTransferChargeCumulatedCurrentYear(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferChargeCumulatedCurrentYear(), 1251105)

    def test_getElectricalEnergySystemTransferChargeCumulatedLifeCycle(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferChargeCumulatedLifeCycle(), 1879163)

    def test_getElectricalEnergySystemTransferDischargeCumulatedUnit(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedUnit(), "wattHour")

    def test_getElectricalEnergySystemTransferDischargeCumulatedCurrentDay(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedCurrentDay(), 3197)

    def test_getElectricalEnergySystemTransferDischargeCumulatedCurrentWeek(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedCurrentWeek(), 3198)

    def test_getElectricalEnergySystemTransferDischargeCumulatedCurrentMonth(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedCurrentMonth(), 136292)

    def test_getElectricalEnergySystemTransferDischargeCumulatedCurrentYear(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedCurrentYear(), 1197530)

    def test_getElectricalEnergySystemTransferDischargeCumulatedLifeCycle(self):
        self.assertEqual(self.device.getElectricalEnergySystemTransferDischargeCumulatedLifeCycle(), 1801122)

    def test_getElectricalEnergySystemSOC(self):
        self.assertEqual(self.device.getElectricalEnergySystemSOC(), 84)

    def test_getElectricalEnergySystemSOCUnit(self):
        self.assertEqual(self.device.getElectricalEnergySystemSOCUnit(), "percent")

    def test_getElectricalEnergySystemPower(self):
        self.assertEqual(self.device.getElectricalEnergySystemPower(), 522)

    def test_getElectricalEnergySystemPowerUnit(self):
        self.assertEqual(self.device.getElectricalEnergySystemPowerUnit(), "watt")

    def test_getElectricalEnergySystemOperationState(self):
        self.assertEqual(self.device.getElectricalEnergySystemOperationState(), "discharge")
