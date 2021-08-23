from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleNotSupported


class FuelCell(Device):

    @handleNotSupported
    def getOperatingPhase(self):
        # generation, startup, standby
        return self.service.getProperty("heating.fuelCell.operating.phase")["properties"]["value"]["value"]

    @handleNotSupported
    def getOperatingModesActive(self):
        # standby, maintenance, heatControlled, economical, ecological
        return self.service.getProperty("heating.fuelCell.operating.modes.active")["properties"]["value"]["value"]

    @handleNotSupported
    def getOperatingModesHeatControlled(self):
        # True or False
        return self.service.getProperty("heating.fuelCell.operating.modes.heatControlled")["properties"]["active"]["value"]

    @handleNotSupported
    def getOperatingModesEcological(self):
        # True or False
        return self.service.getProperty("heating.fuelCell.operating.modes.ecological")["properties"]["active"]["value"]

    @handleNotSupported
    def getOperatingModesEconomical(self):
        # True or False
        return self.service.getProperty("heating.fuelCell.operating.modes.economical")["properties"]["active"]["value"]

    @handleNotSupported
    def getOperatingModesMaintenance(self):
        # True or False
        return self.service.getProperty("heating.fuelCell.operating.modes.maintenance")["properties"]["active"]["value"]

    @handleNotSupported
    def getOperatingModesStandby(self):
        # True or False
        return self.service.getProperty("heating.fuelCell.operating.modes.standby")["properties"]["active"]["value"]

    @handleNotSupported
    def getFuelCellOperationHours(self):
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["operationHours"]["value"]

    @handleNotSupported
    def getFuelCellInsertions(self):
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["insertions"]["value"]

    @handleNotSupported
    def getFuelCellProductionHours(self):
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["productionHours"]["value"]

    @handleNotSupported
    def getFuelCellProductionStarts(self):
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["productionStarts"]["value"]

    @handleNotSupported
    def getFuelCellAvailabilityRate(self):
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["availabilityRate"]["value"]

    @handleNotSupported
    def getCumulativePowerProduced(self):
        return self.service.getProperty("heating.power.production.cumulative")["properties"]["value"]["value"]

    @handleNotSupported
    def getCumulativePowerSold(self):
        return self.service.getProperty("heating.power.sold.cumulative")["properties"]["value"]["value"]

    @handleNotSupported
    def getCumulativePowerPurchased(self):
        return self.service.getProperty("heating.power.purchase.cumulative")["properties"]["value"]["value"]

    @handleNotSupported
    def getFuelCellReturnTemperature(self):
        return self.service.getProperty("heating.fuelCell.sensors.temperature.return")["properties"]["value"]["value"]

    @handleNotSupported
    def getReturnTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]

    @handleNotSupported
    def getPowerProductionCurrent(self):
        return self.service.getProperty("heating.power.production.current")["properties"]["value"]["value"]

    @handleNotSupported
    def getPowerPurchaseCurrent(self):
        return self.service.getProperty("heating.power.purchase.current")["properties"]["value"]["value"]

    @handleNotSupported
    def getPowerOutput(self):
        return self.service.getProperty("heating.sensors.power.output")["properties"]["value"]["value"]

    @handleNotSupported
    def getPowerProductionDemandCoverageCurrent(self):
        return self.service.getProperty("heating.power.production.demandCoverage.current")["properties"]["value"]["value"]

    @handleNotSupported
    def getPowerProductionProductionCoverageCurrent(self):
        return self.service.getProperty("heating.power.production.productionCoverage.current")["properties"]["value"]["value"]

    @handleNotSupported
    def getPowerSoldCurrent(self):
        return self.service.getProperty('heating.power.sold.current')['properties']['value']['value']

    @handleNotSupported
    def getPowerSoldDays(self):
        return self.service.getProperty('heating.power.sold')['properties']['day']['value']

    @handleNotSupported
    def getPowerSoldToday(self):
        return self.service.getProperty('heating.power.sold')['properties']['day']['value'][0]

    @handleNotSupported
    def getPowerSoldWeeks(self):
        return self.service.getProperty('heating.power.sold')['properties']['week']['value']

    @handleNotSupported
    def getPowerSoldThisWeek(self):
        return self.service.getProperty('heating.power.sold')['properties']['week']['value'][0]

    @handleNotSupported
    def getPowerSoldMonths(self):
        return self.service.getProperty('heating.power.sold')['properties']['month']['value']

    @handleNotSupported
    def getPowerSoldThisMonth(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['month']['value'][0]

    @handleNotSupported
    def getPowerSoldYears(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value']

    @handleNotSupported
    def getPowerSoldThisYear(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value'][0]

    @handleNotSupported
    def getPowerProductionDays(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['day']['value']

    @handleNotSupported
    def getPowerProductionToday(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['day']['value'][0]

    @handleNotSupported
    def getPowerProductionWeeks(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['week']['value']

    @handleNotSupported
    def getPowerProductionThisWeek(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['week']['value'][0]

    @handleNotSupported
    def getPowerProductionMonths(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['month']['value']

    @handleNotSupported
    def getPowerProductionThisMonth(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['month']['value'][0]

    @handleNotSupported
    def getPowerProductionYears(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value']

    @handleNotSupported
    def getPowerProductionThisYear(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value'][0]

    @handleNotSupported
    def getPowerConsumptionDays(self):
        return self.service.getProperty('heating.power.consumption')['properties']['day']['value']

    @handleNotSupported
    def getPowerConsumptionToday(self):
        return self.service.getProperty('heating.power.consumption')['properties']['day']['value'][0]

    @handleNotSupported
    def getPowerConsumptionWeeks(self):
        return self.service.getProperty('heating.power.consumption')['properties']['week']['value']

    @handleNotSupported
    def getPowerConsumptionThisWeek(self):
        return self.service.getProperty('heating.power.consumption')['properties']['week']['value'][0]

    @handleNotSupported
    def getPowerConsumptionMonths(self):
        return self.service.getProperty('heating.power.consumption')['properties']['month']['value']

    @handleNotSupported
    def getPowerConsumptionThisMonth(self):
        return self.service.getProperty('heating.power.consumption')['properties']['month']['value'][0]

    @handleNotSupported
    def getPowerConsumptionYears(self):
        return self.service.getProperty('heating.power.consumption')['properties']['year']['value']

    @handleNotSupported
    def getPowerConsumptionThisYear(self):
        return self.service.getProperty('heating.power.consumption')['properties']['year']['value'][0]

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
    def getGasConsumptionFuelCellDays(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['day']['value']

    @handleNotSupported
    def getGasConsumptionFuelCellToday(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['day']['value'][0]

    @handleNotSupported
    def getGasConsumptionFuelCellWeeks(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['week']['value']

    @handleNotSupported
    def getGasConsumptionFuelCellThisWeek(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['week']['value'][0]

    @handleNotSupported
    def getGasConsumptionFuelCellMonths(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['month']['value']

    @handleNotSupported
    def getGasConsumptionFuelCellThisMonth(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['month']['value'][0]

    @handleNotSupported
    def getGasConsumptionFuelCellYears(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['year']['value']

    @handleNotSupported
    def getGasConsumptionFuelCellThisYear(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['year']['value'][0]

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
    def getPowerProductionCoverageTotalDays(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['day']['value']

    @handleNotSupported
    def getPowerProductionCoverageTotalToday(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['day']['value'][0]

    @handleNotSupported
    def getPowerProductionCoverageTotalWeeks(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['week']['value']

    @handleNotSupported
    def getPowerProductionCoverageTotalThisWeek(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['week']['value'][0]

    @handleNotSupported
    def getPowerProductionCoverageTotalMonths(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['month']['value']

    @handleNotSupported
    def getPowerProductionCoverageTotalThisMonth(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['month']['value'][0]

    @handleNotSupported
    def getPowerProductionCoverageTotalYears(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['year']['value']

    @handleNotSupported
    def getPowerProductionCoverageTotalThisYear(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['year']['value'][0]

    @handleNotSupported
    def getHeatProductionDays(self):
        return self.service.getProperty('heating.heat.production')['properties']['day']['value']

    @handleNotSupported
    def getHeatProductionToday(self):
        return self.service.getProperty('heating.heat.production')['properties']['day']['value'][0]

    @handleNotSupported
    def getHeatProductionWeeks(self):
        return self.service.getProperty('heating.heat.production')['properties']['week']['value']

    @handleNotSupported
    def getHeatProductionThisWeek(self):
        return self.service.getProperty('heating.heat.production')['properties']['week']['value'][0]

    @handleNotSupported
    def getHeatProductionMonths(self):
        return self.service.getProperty('heating.heat.production')['properties']['month']['value']

    @handleNotSupported
    def getHeatProductionThisMonth(self):
        return self.service.getProperty('heating.heat.production')['properties']['month']['value'][0]

    @handleNotSupported
    def getHeatProductionYears(self):
        return self.service.getProperty('heating.heat.production')['properties']['year']['value']

    @handleNotSupported
    def getHeatProductionThisYear(self):
        return self.service.getProperty('heating.heat.production')['properties']['year']['value'][0]
