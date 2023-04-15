from typing import Any, List

from PyViCare.PyViCareHeatingDevice import (HeatingDevice,
                                            HeatingDeviceWithComponent,
                                            get_available_burners)
from PyViCare.PyViCareUtils import handleNotSupported


class FuelCell(HeatingDevice):

    @property
    def burners(self) -> List[Any]:
        return list([self.getBurner(x) for x in self.getAvailableBurners()])

    def getBurner(self, burner):
        return FuelCellBurner(self, burner)

    @handleNotSupported
    def getAvailableBurners(self):
        return get_available_burners(self.service)

    @handleNotSupported
    def getReturnTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]

    @handleNotSupported
    def getPowerConsumptionUnit(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["day"]["unit"]

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
        return self.service.getProperty("heating.power.consumption.heating")["properties"]["day"]["unit"]

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
        return self.service.getProperty("heating.gas.consumption.total")["properties"]["day"]["unit"]

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
        return self.service.getProperty("heating.sensors.volumetricFlow.allengra")["properties"]["value"]["value"]

    @handleNotSupported
    def getDomesticHotWaterMaxTemperatureLevel(self):
        return self.service.getProperty("heating.dhw.temperature.levels")["properties"]["max"]["value"]

    @handleNotSupported
    def getDomesticHotWaterMinTemperatureLevel(self):
        return self.service.getProperty("heating.dhw.temperature.levels")["properties"]["min"]["value"]

    @handleNotSupported
    def getHydraulicSeparatorTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.hydraulicSeparator")["properties"]["value"]["value"]

    # ---- Actual FuelCell-relevant methods (they require paid "Advanced" API plan):

    @handleNotSupported
    def getFuelCellOperatingModeActive(self):
        # Returns currently active operating mode as string, e.g. "economical"
        return self.service.getProperty("heating.fuelCell.operating.modes.active")["properties"]["value"]["value"]

    @handleNotSupported
    def getFuelCellPowerProductionUnit(self):
        # Returns the unit for the fuel cell's power production statistics, e.g. kilowattHour
        return self.service.getProperty("heating.fuelCell.power.production")["properties"]["day"]["unit"]

    @handleNotSupported
    def getFuelCellPowerProductionDays(self):
        return self.service.getProperty("heating.fuelCell.power.production")["properties"]["day"]["value"]

    @handleNotSupported
    def getFuelCellPowerProductionToday(self):
        return self.service.getProperty("heating.fuelCell.power.production")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getFuelCellPowerProductionWeeks(self):
        return self.service.getProperty("heating.fuelCell.power.production")["properties"]["week"]["value"]

    @handleNotSupported
    def getFuelCellPowerProductionThisWeek(self):
        return self.service.getProperty("heating.fuelCell.power.production")["properties"]["week"]["value"][0]

    @handleNotSupported
    def getFuelCellPowerProductionMonths(self):
        return self.service.getProperty("heating.fuelCell.power.production")["properties"]["month"]["value"]

    @handleNotSupported
    def getFuelCellPowerProductionThisMonth(self):
        return self.service.getProperty("heating.fuelCell.power.production")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getFuelCellPowerProductionYears(self):
        return self.service.getProperty("heating.fuelCell.power.production")["properties"]["year"]["value"]

    @handleNotSupported
    def getFuelCellPowerProductionThisYear(self):
        return self.service.getProperty("heating.fuelCell.power.production")["properties"]["year"]["value"][0]

    @handleNotSupported
    def getFuelCellOperatingPhase(self):
        # Returns current operating phase as string, e.g. "standby" or "generation"
        return self.service.getProperty("heating.fuelCell.operating.phase")["properties"]["value"]["value"]

    @handleNotSupported
    def getFuelCellPowerProductionCurrentUnit(self):
        # Returns current power production unit, e.g. "watt"
        return self.service.getProperty("heating.power.production.current")["properties"]["value"]["unit"]

    @handleNotSupported
    def getFuelCellPowerProductionCurrent(self):
        # Returns current power production
        return self.service.getProperty("heating.power.production.current")["properties"]["value"]["value"]

    @handleNotSupported
    def getFuelCellPowerPurchaseCurrentUnit(self):
        # Returns current purchased power unit, e.g. "watt"
        return self.service.getProperty("heating.power.purchase.current")["properties"]["value"]["unit"]

    @handleNotSupported
    def getFuelCellPowerPurchaseCurrent(self):
        # Returns current purchased power
        return self.service.getProperty("heating.power.purchase.current")["properties"]["value"]["value"]

    @handleNotSupported
    def getFuelCellPowerSoldCurrentUnit(self):
        # Returns current sold power unit, e.g. "watt"
        return self.service.getProperty("heating.power.sold.current")["properties"]["value"]["unit"]

    @handleNotSupported
    def getFuelCellPowerSoldCurrent(self):
        # Returns current sold power
        return self.service.getProperty("heating.power.sold.current")["properties"]["value"]["value"]

    @handleNotSupported
    def getFuelCellPowerProductionCumulativeUnit(self):
        # Returns cumulated value of produced power unit, e.g. "kilowattHour"
        return self.service.getProperty("heating.power.production.cumulative")["properties"]["value"]["unit"]

    @handleNotSupported
    def getFuelCellPowerProductionCumulative(self):
        # Returns cumulated value of produced power
        return self.service.getProperty("heating.power.production.cumulative")["properties"]["value"]["value"]

    @handleNotSupported
    def getFuelCellPowerPurchaseCumulativeUnit(self):
        # Returns cumulated value of purchased power unit, e.g. "kilowattHour"
        return self.service.getProperty("heating.power.purchase.cumulative")["properties"]["value"]["unit"]

    @handleNotSupported
    def getFuelCellPowerPurchaseCumulative(self):
        # Returns cumulated value of purchased power
        return self.service.getProperty("heating.power.purchase.cumulative")["properties"]["value"]["value"]

    @handleNotSupported
    def getFuelCellPowerSoldCumulativeUnit(self):
        # Returns cumulated value of sold power unit, e.g. "kilowattHour"
        return self.service.getProperty("heating.power.sold.cumulative")["properties"]["value"]["unit"]

    @handleNotSupported
    def getFuelCellPowerSoldCumulative(self):
        # Returns cumulated value of sold power
        return self.service.getProperty("heating.power.sold.cumulative")["properties"]["value"]["value"]

    @handleNotSupported
    def getFuelCellFlowReturnTemperatureUnit(self):
        # Returns flow return temperature unit, e.g. "celsius"
        return self.service.getProperty("heating.fuelCell.sensors.temperature.return")["properties"]["value"]["unit"]

    @handleNotSupported
    def getFuelCellFlowReturnTemperature(self):
        # Returns flow return temperature at the fuel cell as float
        return self.service.getProperty("heating.fuelCell.sensors.temperature.return")["properties"]["value"]["value"]

    @handleNotSupported
    def getFuelCellFlowSupplyTemperatureUnit(self):
        # Returns flow supply temperature unit, e.g. "celsius"
        return self.service.getProperty("heating.fuelCell.sensors.temperature.supply")["properties"]["value"]["unit"]

    @handleNotSupported
    def getFuelCellFlowSupplyTemperature(self):
        # Returns flow supply temperature at the fuel cell as float
        return self.service.getProperty("heating.fuelCell.sensors.temperature.supply")["properties"]["value"]["value"]

    @handleNotSupported
    def getFuelCellOperationHours(self):
        # Returns the operation hours of the fuel cell
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["operationHours"]["value"]

    @handleNotSupported
    def getFuelCellProductionHours(self):
        # Returns the production hours of the fuel cell
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["productionHours"]["value"]

    @handleNotSupported
    def getFuelCellProductionStarts(self):
        # Returns the number of production starts of the fuel cell
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["productionStarts"]["value"]

    @handleNotSupported
    def getFuelCellGasConsumptionUnit(self):
        # Returns the unit for the fuel cell's gas consumption statistics, e.g. "cubicMeter"
        return self.service.getProperty("heating.gas.consumption.fuelCell")["properties"]["day"]["unit"]

    @handleNotSupported
    def getFuelCellGasConsumptionDays(self):
        return self.service.getProperty("heating.gas.consumption.fuelCell")["properties"]["day"]["value"]

    @handleNotSupported
    def getFuelCellGasConsumptionToday(self):
        return self.service.getProperty("heating.gas.consumption.fuelCell")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getFuelCellGasConsumptionWeeks(self):
        return self.service.getProperty("heating.gas.consumption.fuelCell")["properties"]["week"]["value"]

    @handleNotSupported
    def getFuelCellGasConsumptionThisWeek(self):
        return self.service.getProperty("heating.gas.consumption.fuelCell")["properties"]["week"]["value"][0]

    @handleNotSupported
    def getFuelCellGasConsumptionMonths(self):
        return self.service.getProperty("heating.gas.consumption.fuelCell")["properties"]["month"]["value"]

    @handleNotSupported
    def getFuelCellGasConsumptionThisMonth(self):
        return self.service.getProperty("heating.gas.consumption.fuelCell")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getFuelCellGasConsumptionYears(self):
        return self.service.getProperty("heating.gas.consumption.fuelCell")["properties"]["year"]["value"]

    @handleNotSupported
    def getFuelCellGasConsumptionThisYear(self):
        return self.service.getProperty("heating.gas.consumption.fuelCell")["properties"]["year"]["value"][0]


class FuelCellBurner(HeatingDeviceWithComponent):

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
