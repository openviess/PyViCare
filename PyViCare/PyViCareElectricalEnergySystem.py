from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleNotSupported


class ElectricalEnergySystem(Device):

    @handleNotSupported
    def getPointOfCommonCouplingTransferPowerExchange(self):
        return self.service.getProperty("pcc.transfer.power.exchange")["properties"][
            "value"
        ]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedUnit(self):
        return self.service.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["currentDay"]["unit"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedCurrentDay(self):
        return self.service.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["currentDay"]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedCurrentWeek(self):
        return self.service.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["currentWeek"]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedCurrentMonth(self):
        return self.service.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["currentMonth"]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedCurrentYear(self):
        return self.service.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["currentYear"]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedLifeCycle(self):
        return self.service.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["lifeCycle"]["value"]

    @handleNotSupported
    def getPhotovoltaicStatus(self):
        return self.service.getProperty("photovoltaic.status")["properties"]["status"][
            "value"
        ]

    @handleNotSupported
    def getPhotovoltaicProductionCurrent(self):
        return self.service.getProperty("photovoltaic.production.current")[
            "properties"
        ]["value"]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCurrentUnit(self):
        return self.service.getProperty("photovoltaic.production.current")[
            "properties"
        ]["value"]["unit"]

    @handleNotSupported
    def getPointOfCommonCouplingTransferConsumptionTotal(self):
        return self.service.getProperty("pcc.transfer.consumption.total")["properties"][
            "value"
        ]["value"]

    @handleNotSupported
    def getPointOfCommonCouplingTransferConsumptionTotalUnit(self):
        return self.service.getProperty("pcc.transfer.consumption.total")["properties"][
            "value"
        ]["unit"]

    @handleNotSupported
    def getPointOfCommonCouplingTransferFeedInTotal(self):
        return self.service.getProperty("pcc.transfer.feedIn.total")["properties"][
            "value"
        ]["value"]

    @handleNotSupported
    def getPointOfCommonCouplingTransferFeedInTotalUnit(self):
        return self.service.getProperty("pcc.transfer.feedIn.total")["properties"][
            "value"
        ]["unit"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedUnit(self):
        return self.service.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["currentDay"]["unit"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedCurrentDay(self):
        return self.service.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["currentDay"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedCurrentWeek(self):
        return self.service.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["currentWeek"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedCurrentMonth(self):
        return self.service.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["currentMonth"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedCurrentYear(self):
        return self.service.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["currentYear"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedLifeCycle(self):
        return self.service.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["lifeCycle"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemSOC(self):
        return self.service.getProperty("ess.stateOfCharge")["properties"]["value"][
            "value"
        ]

    @handleNotSupported
    def getElectricalEnergySystemSOCUnit(self):
        return self.service.getProperty("ess.stateOfCharge")["properties"]["value"][
            "unit"
        ]

    @handleNotSupported
    def getElectricalEnergySystemPower(self):
        return self.service.getProperty("ess.power")["properties"]["value"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemPowerUnit(self):
        return self.service.getProperty("ess.power")["properties"]["value"]["unit"]

    @handleNotSupported
    def getElectricalEnergySystemOperationState(self):
        return self.service.getProperty("ess.operationState")["properties"]["value"][
            "value"
        ]
