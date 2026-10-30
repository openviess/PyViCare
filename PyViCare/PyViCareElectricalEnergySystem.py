from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleAPICommandErrors, handleNotSupported


class ElectricalEnergySystem(Device):

    @handleNotSupported
    def getPointOfCommonCouplingTransferPowerExchange(self):
        return self.getProperty("pcc.transfer.power.exchange")["properties"][
            "value"
        ]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedUnit(self):
        return self.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["currentDay"]["unit"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedCurrentDay(self):
        return self.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["currentDay"]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedCurrentWeek(self):
        return self.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["currentWeek"]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedCurrentMonth(self):
        return self.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["currentMonth"]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedCurrentYear(self):
        return self.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["currentYear"]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCumulatedLifeCycle(self):
        return self.getProperty("photovoltaic.production.cumulated")[
            "properties"
        ]["lifeCycle"]["value"]

    @handleNotSupported
    def getPhotovoltaicStatus(self):
        return self.getProperty("photovoltaic.status")["properties"]["status"][
            "value"
        ]

    @handleNotSupported
    def getPhotovoltaicInstalledPeakPower(self):
        return self.getProperty("photovoltaic.installedPeakPower")["properties"][
            "value"
        ]["value"]

    @handleNotSupported
    def getPhotovoltaicInstalledPeakPowerUnit(self):
        return self.getProperty("photovoltaic.installedPeakPower")["properties"][
            "value"
        ]["unit"]

    @handleNotSupported
    def getPhotovoltaicStrings(self):
        return self.getProperty("photovoltaic.string")["properties"]["enabled"][
            "value"
        ]

    @handleNotSupported
    def getPhotovoltaicStringName(self, string):
        return self.getProperty(f"photovoltaic.string.{string}")["properties"][
            "name"
        ]["value"]

    @handleNotSupported
    def getPhotovoltaicStringPower(self, string):
        return self.getProperty(f"photovoltaic.string.{string}.power")["properties"][
            "value"
        ]["value"]

    @handleNotSupported
    def getPhotovoltaicStringPowerUnit(self, string):
        return self.getProperty(f"photovoltaic.string.{string}.power")["properties"][
            "value"
        ]["unit"]

    @handleNotSupported
    def getPhotovoltaicStringVoltage(self, string):
        return self.getProperty(f"photovoltaic.string.{string}.voltage")["properties"][
            "value"
        ]["value"]

    @handleNotSupported
    def getPhotovoltaicStringCurrent(self, string):
        return self.getProperty(f"photovoltaic.string.{string}.electricity")[
            "properties"
        ]["value"]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCurrent(self):
        return self.getProperty("photovoltaic.production.current")[
            "properties"
        ]["value"]["value"]

    @handleNotSupported
    def getPhotovoltaicProductionCurrentUnit(self):
        return self.getProperty("photovoltaic.production.current")[
            "properties"
        ]["value"]["unit"]

    @handleNotSupported
    def getPointOfCommonCouplingTransferConsumptionTotal(self):
        return self.getProperty("pcc.transfer.consumption.total")["properties"][
            "value"
        ]["value"]

    @handleNotSupported
    def getPointOfCommonCouplingTransferConsumptionTotalUnit(self):
        return self.getProperty("pcc.transfer.consumption.total")["properties"][
            "value"
        ]["unit"]

    @handleNotSupported
    def getPointOfCommonCouplingTransferFeedInTotal(self):
        return self.getProperty("pcc.transfer.feedIn.total")["properties"][
            "value"
        ]["value"]

    @handleNotSupported
    def getPointOfCommonCouplingTransferFeedInTotalUnit(self):
        return self.getProperty("pcc.transfer.feedIn.total")["properties"][
            "value"
        ]["unit"]

    @handleNotSupported
    def getElectricalEnergySystemTransferChargeCumulatedUnit(self):
        return self.getProperty("ess.transfer.charge.cumulated")[
            "properties"
        ]["currentDay"]["unit"]

    @handleNotSupported
    def getElectricalEnergySystemTransferChargeCumulatedCurrentDay(self):
        return self.getProperty("ess.transfer.charge.cumulated")[
            "properties"
        ]["currentDay"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferChargeCumulatedCurrentWeek(self):
        return self.getProperty("ess.transfer.charge.cumulated")[
            "properties"
        ]["currentWeek"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferChargeCumulatedCurrentMonth(self):
        return self.getProperty("ess.transfer.charge.cumulated")[
            "properties"
        ]["currentMonth"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferChargeCumulatedCurrentYear(self):
        return self.getProperty("ess.transfer.charge.cumulated")[
            "properties"
        ]["currentYear"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferChargeCumulatedLifeCycle(self):
        return self.getProperty("ess.transfer.charge.cumulated")[
            "properties"
        ]["lifeCycle"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedUnit(self):
        return self.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["currentDay"]["unit"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedCurrentDay(self):
        return self.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["currentDay"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedCurrentWeek(self):
        return self.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["currentWeek"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedCurrentMonth(self):
        return self.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["currentMonth"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedCurrentYear(self):
        return self.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["currentYear"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemTransferDischargeCumulatedLifeCycle(self):
        return self.getProperty("ess.transfer.discharge.cumulated")[
            "properties"
        ]["lifeCycle"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemSOC(self):
        return self.getProperty("ess.stateOfCharge")["properties"]["value"][
            "value"
        ]

    @handleNotSupported
    def getElectricalEnergySystemSOCUnit(self):
        return self.getProperty("ess.stateOfCharge")["properties"]["value"][
            "unit"
        ]

    @handleNotSupported
    def getElectricalEnergySystemPower(self):
        return self.getProperty("ess.power")["properties"]["value"]["value"]

    @handleNotSupported
    def getElectricalEnergySystemPowerUnit(self):
        return self.getProperty("ess.power")["properties"]["value"]["unit"]

    @handleNotSupported
    def getElectricalEnergySystemOperationState(self):
        return self.getProperty("ess.operationState")["properties"]["value"][
            "value"
        ]

    @handleNotSupported
    def getElectricalEnergySystemBatteryControlMode(self):
        return self.getProperty("ess.battery.control.mode.active")["properties"][
            "value"
        ]["value"]

    @handleNotSupported
    def getElectricalEnergySystemBatteryControlModes(self):
        return self.getProperty("ess.battery.control.mode.active")["commands"][
            "setMode"
        ]["params"]["value"]["constraints"]["enum"]

    @handleAPICommandErrors
    def setElectricalEnergySystemBatteryControlMode(self, mode: str):
        return self.setProperty(
            "ess.battery.control.mode.active", "setMode", {"value": mode}
        )
