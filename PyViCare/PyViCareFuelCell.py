from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCare import handleKeyError

class FuelCell(GazBoiler):

    @handleKeyError
    def getOperatingPhase(self):
        # generation, startup, standby
        return self.service.getProperty("heating.fuelCell.operating.phase")["properties"]["value"]["value"]

    @handleKeyError
    def getOperatingModesActive(self):
        # standby, maintenance, heatControlled, economical, ecological
        return self.service.getProperty("heating.fuelCell.operating.modes.active")["properties"]["value"]["value"]

    @handleKeyError
    def getOperatingModesHeatControlled(self):
        # True or False
        return self.service.getProperty("heating.fuelCell.operating.modes.heatControlled")["properties"]["active"]["value"]    

    @handleKeyError
    def getOperatingModesEcological(self):
        # True or False
        return self.service.getProperty("heating.fuelCell.operating.modes.ecological")["properties"]["active"]["value"]

    @handleKeyError
    def getOperatingModesEconomical(self):
        # True or False
        return self.service.getProperty("heating.fuelCell.operating.modes.economical")["properties"]["active"]["value"]

    @handleKeyError
    def getOperatingModesMaintenance(self):
        # True or False
        return self.service.getProperty("heating.fuelCell.operating.modes.maintenance")["properties"]["active"]["value"]

    @handleKeyError
    def getOperatingModesStandby(self):
        # True or False
        return self.service.getProperty("heating.fuelCell.operating.modes.standby")["properties"]["active"]["value"]

    @handleKeyError
    def getFuelCellOperationHours(self):
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["operationHours"]["value"]

    @handleKeyError
    def getFuelCellInsertions(self):
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["insertions"]["value"]

    @handleKeyError
    def getFuelCellProductionHours(self):
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["productionHours"]["value"]

    @handleKeyError
    def getFuelCellProductionStarts(self):
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["productionStarts"]["value"]

    @handleKeyError
    def getFuelCellAvailabilityRate(self):
        return self.service.getProperty("heating.fuelCell.statistics")["properties"]["availabilityRate"]["value"]

    @handleKeyError
    def getCumulativePowerProduced(self):
        return self.service.getProperty("heating.power.cumulativeProduced")["properties"]["value"]["value"]

    @handleKeyError
    def getCumulativePowerSold(self):
        return self.service.getProperty("heating.power.cumulativeSold")["properties"]["value"]["value"]

    @handleKeyError
    def getCumulativePowerPurchased(self):
        return self.service.getProperty("heating.power.cumulativePurchased")["properties"]["value"]["value"]

    @handleKeyError
    def getFuelCellReturnTemperature(self):
        return self.service.getProperty("heating.fuelCell.sensors.temperature.return")["properties"]["value"]["value"]

    @handleKeyError
    def getReturnTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]

    @handleKeyError
    def getPowerProductionCurrent(self):
        return self.service.getProperty("heating.power.production.current")["properties"]["value"]["value"]

    @handleKeyError
    def getPowerPurchaseCurrent(self):
        return self.service.getProperty("heating.power.purchase.current")["properties"]["value"]["value"]

    @handleKeyError
    def getPowerOutput(self):
        return self.service.getProperty("heating.sensors.power.output")["properties"]["value"]["value"]

    @handleKeyError
    def getPowerProductionDemandCoverageCurrent(self):
        return self.service.getProperty("heating.power.production.demandCoverage.current")["properties"]["value"]["value"]

    @handleKeyError
    def getPowerProductionProductionCoverageCurrent(self):
        return self.service.getProperty("heating.power.production.productionCoverage.current")["properties"]["value"]["value"]

    @handleKeyError
    def getPowerSoldCurrent(self):
        return self.service.getProperty('heating.power.sold.current')['properties']['value']['value']

    @handleKeyError
    def getPowerSoldDays(self):
        return self.service.getProperty('heating.power.sold')['properties']['day']['value']

    @handleKeyError
    def getPowerSoldToday(self):
        return self.service.getProperty('heating.power.sold')['properties']['day']['value'][0]

    @handleKeyError
    def getPowerSoldWeeks(self):
        return self.service.getProperty('heating.power.sold')['properties']['week']['value']

    @handleKeyError
    def getPowerSoldThisWeek(self):
        return self.service.getProperty('heating.power.sold')['properties']['week']['value'][0]

    @handleKeyError
    def getPowerSoldMonths(self):
        return self.service.getProperty('heating.power.sold')['properties']['month']['value']

    @handleKeyError
    def getPowerSoldThisMonth(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['month']['value'][0]

    @handleKeyError
    def getPowerSoldYears(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value']

    @handleKeyError
    def getPowerSoldThisYear(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value'][0]

    @handleKeyError
    def getPowerProductionDays(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['day']['value']

    @handleKeyError
    def getPowerProductionToday(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['day']['value'][0]

    @handleKeyError
    def getPowerProductionWeeks(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['week']['value']

    @handleKeyError
    def getPowerProductionThisWeek(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['week']['value'][0]

    @handleKeyError
    def getPowerProductionMonths(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['month']['value']

    @handleKeyError
    def getPowerProductionThisMonth(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['month']['value'][0]

    @handleKeyError
    def getPowerProductionYears(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value']

    @handleKeyError
    def getPowerProductionThisYear(self):
        return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value'][0]

    @handleKeyError
    def getPowerConsumptionDays(self):
        return self.service.getProperty('heating.power.consumption')['properties']['day']['value']

    @handleKeyError
    def getPowerConsumptionToday(self):
        return self.service.getProperty('heating.power.consumption')['properties']['day']['value'][0]

    @handleKeyError
    def getPowerConsumptionWeeks(self):
        return self.service.getProperty('heating.power.consumption')['properties']['week']['value']

    @handleKeyError
    def getPowerConsumptionThisWeek(self):
        return self.service.getProperty('heating.power.consumption')['properties']['week']['value'][0]

    @handleKeyError
    def getPowerConsumptionMonths(self):
        return self.service.getProperty('heating.power.consumption')['properties']['month']['value']

    @handleKeyError
    def getPowerConsumptionThisMonth(self):
        return self.service.getProperty('heating.power.consumption')['properties']['month']['value'][0]

    @handleKeyError
    def getPowerConsumptionYears(self):
        return self.service.getProperty('heating.power.consumption')['properties']['year']['value']

    @handleKeyError
    def getPowerConsumptionThisYear(self):
        return self.service.getProperty('heating.power.consumption')['properties']['year']['value'][0]

    @handleKeyError
    def getPowerConsumptionHeatingDays(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['day']['value']

    @handleKeyError
    def getPowerConsumptionHeatingToday(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['day']['value'][0]

    @handleKeyError
    def getPowerConsumptionHeatingWeeks(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['week']['value']

    @handleKeyError
    def getPowerConsumptionHeatingThisWeek(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['week']['value'][0]

    @handleKeyError
    def getPowerConsumptionHeatingMonths(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['month']['value']

    @handleKeyError
    def getPowerConsumptionHeatingThisMonth(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['month']['value'][0]

    @handleKeyError
    def getPowerConsumptionHeatingYears(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['year']['value']

    @handleKeyError
    def getPowerConsumptionHeatingThisYear(self):
        return self.service.getProperty('heating.power.consumption.heating')['properties']['year']['value'][0]

    @handleKeyError
    def getPowerConsumptionDomesticHotWaterDays(self):
        return self.service.getProperty('dhw.power.consumption.dhw')['properties']['day']['value']

    @handleKeyError
    def getPowerConsumptionDomesticHotWaterToday(self):
        return self.service.getProperty('dhw.power.consumption.dhw')['properties']['day']['value'][0]

    @handleKeyError
    def getPowerConsumptionDomesticHotWaterWeeks(self):
        return self.service.getProperty('dhw.power.consumption.dhw')['properties']['week']['value']

    @handleKeyError
    def getPowerConsumptionDomesticHotWaterThisWeek(self):
        return self.service.getProperty('dhw.power.consumption.dhw')['properties']['week']['value'][0]

    @handleKeyError
    def getPowerConsumptionDomesticHotWaterMonths(self):
        return self.service.getProperty('dhw.power.consumption.dhw')['properties']['month']['value']

    @handleKeyError
    def getPowerConsumptionDomesticHotWaterThisMonth(self):
        return self.service.getProperty('dhw.power.consumption.dhw')['properties']['month']['value'][0]

    @handleKeyError
    def getPowerConsumptionDomesticHotWaterYears(self):
        return self.service.getProperty('dhw.power.consumption.dhw')['properties']['year']['value']

    @handleKeyError
    def getPowerConsumptionDomesticHotWaterThisYear(self):
        return self.service.getProperty('dhw.power.consumption.dhw')['properties']['year']['value'][0]

    @handleKeyError
    def getGasConsumptionFuelCellDays(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['day']['value']

    @handleKeyError
    def getGasConsumptionFuelCellToday(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['day']['value'][0]

    @handleKeyError
    def getGasConsumptionFuelCellWeeks(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['week']['value']

    @handleKeyError
    def getGasConsumptionFuelCellThisWeek(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['week']['value'][0]

    @handleKeyError
    def getGasConsumptionFuelCellMonths(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['month']['value']

    @handleKeyError
    def getGasConsumptionFuelCellThisMonth(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['month']['value'][0]

    @handleKeyError
    def getGasConsumptionFuelCellYears(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['year']['value']

    @handleKeyError
    def getGasConsumptionFuelCellThisYear(self):
        return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['year']['value'][0]

    @handleKeyError
    def getGasConsumptionTotalDays(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['day']['value']

    @handleKeyError
    def getGasConsumptionTotalToday(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['day']['value'][0]

    @handleKeyError
    def getGasConsumptionTotalWeeks(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['week']['value']

    @handleKeyError
    def getGasConsumptionTotalThisWeek(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['week']['value'][0]

    @handleKeyError
    def getGasConsumptionTotalMonths(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['month']['value']

    @handleKeyError
    def getGasConsumptionTotalThisMonth(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['month']['value'][0]

    @handleKeyError
    def getGasConsumptionTotalYears(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['year']['value']

    @handleKeyError
    def getGasConsumptionTotalThisYear(self):
        return self.service.getProperty('heating.gas.consumption.total')['properties']['year']['value'][0]

    @handleKeyError
    def getPowerProductionCoverageTotalDays(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['day']['value']

    @handleKeyError
    def getPowerProductionCoverageTotalToday(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['day']['value'][0]

    @handleKeyError
    def getPowerProductionCoverageTotalWeeks(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['week']['value']

    @handleKeyError
    def getPowerProductionCoverageTotalThisWeek(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['week']['value'][0]

    @handleKeyError
    def getPowerProductionCoverageTotalMonths(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['month']['value']

    @handleKeyError
    def getPowerProductionCoverageTotalThisMonth(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['month']['value'][0]

    @handleKeyError
    def getPowerProductionCoverageTotalYears(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['year']['value']

    @handleKeyError
    def getPowerProductionCoverageTotalThisYear(self):
        return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['year']['value'][0]

    @handleKeyError
    def getHeatProductionDays(self):
        return self.service.getProperty('heating.heat.production')['properties']['day']['value']

    @handleKeyError
    def getHeatProductionToday(self):
        return self.service.getProperty('heating.heat.production')['properties']['day']['value'][0]

    @handleKeyError
    def getHeatProductionWeeks(self):
        return self.service.getProperty('heating.heat.production')['properties']['week']['value']

    @handleKeyError
    def getHeatProductionThisWeek(self):
        return self.service.getProperty('heating.heat.production')['properties']['week']['value'][0]

    @handleKeyError
    def getHeatProductionMonths(self):
        return self.service.getProperty('heating.heat.production')['properties']['month']['value']

    @handleKeyError
    def getHeatProductionThisMonth(self):
        return self.service.getProperty('heating.heat.production')['properties']['month']['value'][0]

    @handleKeyError
    def getHeatProductionYears(self):
        return self.service.getProperty('heating.heat.production')['properties']['year']['value']

    @handleKeyError
    def getHeatProductionThisYear(self):
        return self.service.getProperty('heating.heat.production')['properties']['year']['value'][0]
