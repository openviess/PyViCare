from typing import Any, List

from PyViCare.PyViCareDevice import Device, DeviceWithComponent
from PyViCare.PyViCareUtils import handleNotSupported


class GazBoiler(Device):

    @property
    def burners(self) -> List[Any]:
        return list([self.getBurner(x) for x in self.getAvailableBurners()])

    def getBurner(self, burner):
        return GazBurner(self, burner)

    @handleNotSupported
    def getAvailableBurners(self):
        return self.service.getProperty("heating.burners")["components"]

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
    def getDomesticHotWaterChargingLevel(self):
        return self.service.getProperty("heating.dhw.charging.level")["properties"]["value"]["value"]

    @handleNotSupported
    def getBoilerCommonSupplyTemperature(self):
        return self.service.getProperty("heating.boiler.sensors.temperature.commonSupply")["properties"]["value"]["value"]

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


class GazBurner(DeviceWithComponent):

    @property
    def burner(self) -> str:
        return self.component

    @handleNotSupported
    def getIsActive(self):
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
