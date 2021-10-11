from typing import Any, List

from PyViCare.PyViCareDevice import Device, DeviceWithComponent
from PyViCare.PyViCareUtils import handleNotSupported


class FuelCell(Device):

    @property
    def burners(self) -> List[Any]:
        return list([self.getBurner(x) for x in self.getAvailableBurners()])

    def getBurner(self, burner):
        return FuelCellBurner(self, burner)

    @handleNotSupported
    def getAvailableBurners(self):
        return self.service.getProperty("heating.burners")["components"]

    @handleNotSupported
    def getReturnTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]

    @handleNotSupported
    def getPowerConsumptionUnit(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["unit"]["value"]

    @handleNotSupported
    def getPowerConsumptionDays(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['day']['value']

    @handleNotSupported
    def getPowerConsumptionToday(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['day']['value'][0]

    @handleNotSupported
    def getPowerConsumptionWeeks(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['week']['value']

    @handleNotSupported
    def getPowerConsumptionThisWeek(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['week']['value'][0]

    @handleNotSupported
    def getPowerConsumptionMonths(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['month']['value']

    @handleNotSupported
    def getPowerConsumptionThisMonth(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['month']['value'][0]

    @handleNotSupported
    def getPowerConsumptionYears(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['year']['value']

    @handleNotSupported
    def getPowerConsumptionThisYear(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['year']['value'][0]

    @handleNotSupported
    def getPowerConsumptionHeatingUnit(self):
        return self.service.getProperty("heating.power.consumption.heating")["properties"]["unit"]["value"]

    @handleNotSupported
    def getPowerConsumptionHeatingDays(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['day']['value']

    @handleNotSupported
    def getPowerConsumptionHeatingToday(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['day']['value'][0]

    @handleNotSupported
    def getPowerConsumptionHeatingWeeks(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['week']['value']

    @handleNotSupported
    def getPowerConsumptionHeatingThisWeek(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['week']['value'][0]

    @handleNotSupported
    def getPowerConsumptionHeatingMonths(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['month']['value']

    @handleNotSupported
    def getPowerConsumptionHeatingThisMonth(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['month']['value'][0]

    @handleNotSupported
    def getPowerConsumptionHeatingYears(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['year']['value']

    @handleNotSupported
    def getPowerConsumptionHeatingThisYear(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['year']['value'][0]

    @handleNotSupported
    def getGasConsumptionUnit(self):
        return self.service.getProperty("heating.gas.consumption.total")["properties"]["unit"]["value"]

    @handleNotSupported
    def getGasConsumptionTotalDays(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['day']['value']

    @handleNotSupported
    def getGasConsumptionTotalToday(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['day']['value'][0]

    @handleNotSupported
    def getGasConsumptionTotalWeeks(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['week']['value']

    @handleNotSupported
    def getGasConsumptionTotalThisWeek(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['week']['value'][0]

    @handleNotSupported
    def getGasConsumptionTotalMonths(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['month']['value']

    @handleNotSupported
    def getGasConsumptionTotalThisMonth(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['month']['value'][0]

    @handleNotSupported
    def getGasConsumptionTotalYears(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['year']['value']

    @handleNotSupported
    def getGasConsumptionTotalThisYear(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['year']['value'][0]

    @handleNotSupported
    def getVolumetricFlowReturn(self):
        return self.service.getProperty("heating.sensors.volumetricFlow.return")["properties"]["value"]["value"]

    @handleNotSupported
    def getDomesticHotWaterMaxTemperatureLevel(self):
        return self.service.getProperty("heating.dhw.temperature.levels")["properties"]["max"]["value"]

    @handleNotSupported
    def getDomesticHotWaterMinTemperatureLevel(self):
        return self.service.getProperty("heating.dhw.temperature.levels")["properties"]["min"]["value"]

    @handleNotSupported
    def getHydraulicSeparatorTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.hydraulicSeparator")["properties"]["value"]["value"]


class FuelCellBurner(DeviceWithComponent):

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
