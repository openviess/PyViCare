from typing import Any, List

from PyViCare.PyViCareHeatingDevice import (HeatingDevice,
                                            HeatingDeviceWithComponent,
                                            get_available_burners)
from PyViCare.PyViCareUtils import handleNotSupported


class GazBoiler(HeatingDevice):

    @property
    def burners(self) -> List[Any]:
        return list([self.getBurner(x) for x in self.getAvailableBurners()])

    def getBurner(self, burner):
        return GazBurner(self, burner)

    @handleNotSupported
    def getAvailableBurners(self):
        return get_available_burners(self.service)

    @handleNotSupported
    def getGasConsumptionHeatingUnit(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["day"]["unit"]

    @handleNotSupported
    def getGasConsumptionHeatingDays(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["day"]["value"]

    @handleNotSupported
    def getGasConsumptionHeatingToday(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getGasConsumptionHeatingWeeks(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["week"]["value"]

    @handleNotSupported
    def getGasConsumptionHeatingThisWeek(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["week"]["value"][0]

    @handleNotSupported
    def getGasConsumptionHeatingMonths(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["month"]["value"]

    @handleNotSupported
    def getGasConsumptionHeatingThisMonth(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getGasConsumptionHeatingYears(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["year"]["value"]

    @handleNotSupported
    def getGasConsumptionHeatingThisYear(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["year"]["value"][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterUnit(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["day"]["unit"]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterDays(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["day"]["value"]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterToday(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterWeeks(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["week"]["value"]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterThisWeek(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["week"]["value"][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterMonths(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["month"]["value"]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterThisMonth(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterYears(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["year"]["value"]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterThisYear(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["year"]["value"][0]

    @handleNotSupported
    def getBoilerTemperature(self):
        return self.service.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]

    @handleNotSupported
    def getBoilerTargetTemperature(self):
        return self.service.getProperty("heating.boiler.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getDomesticHotWaterChargingLevel(self):
        return self.service.getProperty("heating.dhw.charging.level")["properties"]["value"]["value"]

    @handleNotSupported
    def getBoilerCommonSupplyTemperature(self):
        return self.service.getProperty("heating.boiler.sensors.temperature.commonSupply")["properties"]["value"]["value"]

    @handleNotSupported
    def getPowerConsumptionUnit(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["day"]["unit"]

    @handleNotSupported
    def getPowerConsumptionDays(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["day"]["value"]

    @handleNotSupported
    def getPowerConsumptionToday(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionWeeks(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["week"]["value"]

    @handleNotSupported
    def getPowerConsumptionThisWeek(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["week"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionMonths(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["month"]["value"]

    @handleNotSupported
    def getPowerConsumptionThisMonth(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionYears(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["year"]["value"]

    @handleNotSupported
    def getPowerConsumptionThisYear(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["year"]["value"][0]

    @handleNotSupported
    def getVolumetricFlowReturn(self):
        return self.service.getProperty("heating.sensors.volumetricFlow.allengra")["properties"]["value"]["value"]

    # For Vitodens-100W new "summary" api methods
    # Gas consumption for Heating data:
    @handleNotSupported
    def getGasSummaryConsumptionHeatingUnit(self):
        return self.service.getProperty("heating.gas.consumption.summary.heating")["properties"]["day"]["unit"]

    @handleNotSupported
    def getGasSummaryConsumptionHeatingCurrentDay(self):
        return self.service.getProperty("heating.gas.consumption.summary.heating")["properties"]["currentDay"]["value"]

    @handleNotSupported
    def getGasSummaryConsumptionHeatingCurrentMonth(self):
        return self.service.getProperty("heating.gas.consumption.summary.heating")["properties"]["currentMonth"]["value"]

    @handleNotSupported
    def getGasSummaryConsumptionHeatingCurrentYear(self):
        return self.service.getProperty("heating.gas.consumption.summary.heating")["properties"]["currentYear"]["value"]

    @handleNotSupported
    def getGasSummaryConsumptionHeatingLastMonth(self):
        return self.service.getProperty("heating.gas.consumption.summary.heating")["properties"]["lastMonth"]["value"]

    @handleNotSupported
    def getGasSummaryConsumptionHeatingLastSevenDays(self):
        return self.service.getProperty("heating.gas.consumption.summary.heating")["properties"]["lastSevenDays"]["value"]

    @handleNotSupported
    def getGasSummaryConsumptionHeatingLastYear(self):
        return self.service.getProperty("heating.gas.consumption.summary.heating")["properties"]["lastYear"]["value"]

    # Gas consumption for Domestic Hot Water data:
    @handleNotSupported
    def getGasSummaryConsumptionDomesticHotWaterUnit(self):
        return self.service.getProperty("heating.gas.consumption.summary.dhw")["properties"]["unit"]["value"]

    @handleNotSupported
    def getGasSummaryConsumptionDomesticHotWaterCurrentDay(self):
        return self.service.getProperty("heating.gas.consumption.summary.dhw")["properties"]["currentDay"]["value"]

    @handleNotSupported
    def getGasSummaryConsumptionDomesticHotWaterCurrentMonth(self):
        return self.service.getProperty("heating.gas.consumption.summary.dhw")["properties"]["currentMonth"]["value"]

    @handleNotSupported
    def getGasSummaryConsumptionDomesticHotWaterCurrentYear(self):
        return self.service.getProperty("heating.gas.consumption.summary.dhw")["properties"]["currentYear"]["value"]

    @handleNotSupported
    def getGasSummaryConsumptionDomesticHotWaterLastMonth(self):
        return self.service.getProperty("heating.gas.consumption.summary.dhw")["properties"]["lastMonth"]["value"]

    @handleNotSupported
    def getGasSummaryConsumptionDomesticHotWaterLastSevenDays(self):
        return self.service.getProperty("heating.gas.consumption.summary.dhw")["properties"]["lastSevenDays"]["value"]

    @handleNotSupported
    def getGasSummaryConsumptionDomesticHotWaterLastYear(self):
        return self.service.getProperty("heating.gas.consumption.summary.dhw")["properties"]["lastYear"]["value"]

    # Power consumption for Heating:
    @handleNotSupported
    def getPowerSummaryConsumptionHeatingUnit(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["day"]["unit"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingCurrentDay(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["currentDay"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingCurrentMonth(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["currentMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingCurrentYear(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["currentYear"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingLastMonth(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["lastMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingLastSevenDays(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["lastSevenDays"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingLastYear(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["lastYear"]["value"]

    # Power consumption for Domestic Hot Water:
    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterUnit(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["day"]["unit"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterCurrentDay(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["currentDay"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["currentMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterCurrentYear(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["currentYear"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterLastMonth(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["lastMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["lastSevenDays"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterLastYear(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["lastYear"]["value"]


class GazBurner(HeatingDeviceWithComponent):

    @property
    def burner(self) -> str:
        return self.component

    @handleNotSupported
    def getActive(self):
        return self.service.getProperty(f"heating.burners.{self.burner}")["properties"]["active"]["value"]

    @handleNotSupported
    def getHours(self):
        return self.service.getProperty(f"heating.burners.{self.burner}.statistics")["properties"]["hours"]["value"]

    @handleNotSupported
    def getStarts(self):
        return self.service.getProperty(f"heating.burners.{self.burner}.statistics")["properties"]["starts"]["value"]

    @handleNotSupported
    def getModulation(self):
        return self.service.getProperty(f"heating.burners.{self.burner}.modulation")["properties"]["value"]["value"]
