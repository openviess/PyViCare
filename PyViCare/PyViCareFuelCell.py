from PyViCare.PyViCareGazBoiler import GazBoiler

class FuelCell(GazBoiler):

    def getOperatingPhase(self):
        try:
            # generation, startup, standby
            return self.service.getProperty("heating.fuelCell.operating.phase")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getOperatingModesActive(self):
        try:
            # standby, maintenance, heatControlled, economical, ecological
            return self.service.getProperty("heating.fuelCell.operating.modes.active")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getOperatingModesHeatControlled(self):
        try:
            # True or False
            return self.service.getProperty("heating.fuelCell.operating.modes.heatControlled")["properties"]["active"]["value"]
        except KeyError:
            return "error"

    def getOperatingModesEcological(self):
        try:
            # True or False
            return self.service.getProperty("heating.fuelCell.operating.modes.ecological")["properties"]["active"]["value"]
        except KeyError:
            return "error"

    def getOperatingModesEconomical(self):
        try:
            # True or False
            return self.service.getProperty("heating.fuelCell.operating.modes.economical")["properties"]["active"]["value"]
        except KeyError:
            return "error"

    def getOperatingModesMaintenance(self):
        try:
            # True or False
            return self.service.getProperty("heating.fuelCell.operating.modes.maintenance")["properties"]["active"]["value"]
        except KeyError:
            return "error"

    def getOperatingModesStandby(self):
        try:
            # True or False
            return self.service.getProperty("heating.fuelCell.operating.modes.standby")["properties"]["active"]["value"]
        except KeyError:
            return "error"

    def getFuelCellOperationHours(self):
        try:
            return self.service.getProperty("heating.fuelCell.statistics")["properties"]["operationHours"]["value"]
        except KeyError:
            return "error"

    def getFuelCellInsertions(self):
        try:
            return self.service.getProperty("heating.fuelCell.statistics")["properties"]["insertions"]["value"]
        except KeyError:
            return "error"

    def getFuelCellProductionHours(self):
        try:
            return self.service.getProperty("heating.fuelCell.statistics")["properties"]["productionHours"]["value"]
        except KeyError:
            return "error"

    def getFuelCellProductionStarts(self):
        try:
            return self.service.getProperty("heating.fuelCell.statistics")["properties"]["productionStarts"]["value"]
        except KeyError:
            return "error"

    def getFuelCellAvailabilityRate(self):
        try:
            return self.service.getProperty("heating.fuelCell.statistics")["properties"]["availabilityRate"]["value"]
        except KeyError:
            return "error"

    def getCumulativePowerProduced(self):
        try:
            return self.service.getProperty("heating.power.cumulativeProduced")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getCumulativePowerSold(self):
        try:
            return self.service.getProperty("heating.power.cumulativeSold")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getCumulativePowerPurchased(self):
        try:
            return self.service.getProperty("heating.power.cumulativePurchased")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getFuelCellReturnTemperature(self):
        try:
            return self.service.getProperty("heating.fuelCell.sensors.temperature.return")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getReturnTemperature(self):
        try:
            return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getPowerProductionCurrent(self):
        try:
            return self.service.getProperty("heating.power.production.current")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getPowerPurchaseCurrent(self):
        try:
            return self.service.getProperty("heating.power.purchase.current")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getPowerOutput(self):
        try:
            return self.service.getProperty("heating.sensors.power.output")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getPowerProductionDemandCoverageCurrent(self):
        try:
            return self.service.getProperty("heating.power.production.demandCoverage.current")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getPowerProductionProductionCoverageCurrent(self):
        try:
            return self.service.getProperty("heating.power.production.productionCoverage.current")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getPowerSoldCurrent(self):
        try:
            return self.service.getProperty('heating.power.sold.current')['properties']['value']['value']
        except KeyError:
            return "error"

    def getPowerSoldDays(self):
        try:
            return self.service.getProperty('heating.power.sold')['properties']['day']['value']
        except KeyError:
            return "error"

    def getPowerSoldToday(self):
        try:
            return self.service.getProperty('heating.power.sold')['properties']['day']['value'][0]
        except KeyError:
            return "error"

    def getPowerSoldWeeks(self):
        try:
            return self.service.getProperty('heating.power.sold')['properties']['week']['value']
        except KeyError:
            return "error"

    def getPowerSoldThisWeek(self):
        try:
            return self.service.getProperty('heating.power.sold')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getPowerSoldMonths(self):
        try:
            return self.service.getProperty('heating.power.sold')['properties']['month']['value']
        except KeyError:
            return "error"

    def getPowerSoldThisMonth(self):
        try:
            return self.service.getProperty('heating.fuelCell.power.production')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getPowerSoldYears(self):
        try:
            return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value']
        except KeyError:
            return "error"

    def getPowerSoldThisYear(self):
        try:
            return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value'][0]
        except KeyError:
            return "error"

    def getPowerProductionDays(self):
        try:
            return self.service.getProperty('heating.fuelCell.power.production')['properties']['day']['value']
        except KeyError:
            return "error"

    def getPowerProductionToday(self):
        try:
            return self.service.getProperty('heating.fuelCell.power.production')['properties']['day']['value'][0]
        except KeyError:
            return "error"

    def getPowerProductionWeeks(self):
        try:
            return self.service.getProperty('heating.fuelCell.power.production')['properties']['week']['value']
        except KeyError:
            return "error"

    def getPowerProductionThisWeek(self):
        try:
            return self.service.getProperty('heating.fuelCell.power.production')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getPowerProductionMonths(self):
        try:
            return self.service.getProperty('heating.fuelCell.power.production')['properties']['month']['value']
        except KeyError:
            return "error"

    def getPowerProductionThisMonth(self):
        try:
            return self.service.getProperty('heating.fuelCell.power.production')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getPowerProductionYears(self):
        try:
            return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value']
        except KeyError:
            return "error"

    def getPowerProductionThisYear(self):
        try:
            return self.service.getProperty('heating.fuelCell.power.production')['properties']['year']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionDays(self):
        try:
            return self.service.getProperty('heating.power.consumption')['properties']['day']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionToday(self):
        try:
            return self.service.getProperty('heating.power.consumption')['properties']['day']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionWeeks(self):
        try:
            return self.service.getProperty('heating.power.consumption')['properties']['week']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionThisWeek(self):
        try:
            return self.service.getProperty('heating.power.consumption')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionMonths(self):
        try:
            return self.service.getProperty('heating.power.consumption')['properties']['month']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionThisMonth(self):
        try:
            return self.service.getProperty('heating.power.consumption')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionYears(self):
        try:
            return self.service.getProperty('heating.power.consumption')['properties']['year']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionThisYear(self):
        try:
            return self.service.getProperty('heating.power.consumption')['properties']['year']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingDays(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['day']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingToday(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['day']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingWeeks(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['week']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingThisWeek(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingMonths(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['month']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingThisMonth(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingYears(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['year']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingThisYear(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['year']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterDays(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['day']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterToday(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['day']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterWeeks(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['week']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterThisWeek(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterMonths(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['month']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterThisMonth(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterYears(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['year']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterThisYear(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['year']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterThisWeek(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterMonths(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['month']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterThisMonth(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterYears(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['year']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionDomesticHotWaterThisYear(self):
        try:
            return self.service.getProperty('dhw.power.consumption.dhw')['properties']['year']['value'][0]
        except KeyError:
            return "error"


    def getPowerConsumptionHeatingThisWeek(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingMonths(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['month']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingThisMonth(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingYears(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['year']['value']
        except KeyError:
            return "error"

    def getPowerConsumptionHeatingThisYear(self):
        try:
            return self.service.getProperty('heating.power.consumption.heating')['properties']['year']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionFuelCellDays(self):
        try:
            return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['day']['value']
        except KeyError:
            return "error"

    def getGasConsumptionFuelCellToday(self):
        try:
            return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['day']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionFuelCellWeeks(self):
        try:
            return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['week']['value']
        except KeyError:
            return "error"

    def getGasConsumptionFuelCellThisWeek(self):
        try:
            return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionFuelCellMonths(self):
        try:
            return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['month']['value']
        except KeyError:
            return "error"

    def getGasConsumptionFuelCellThisMonth(self):
        try:
            return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionFuelCellYears(self):
        try:
            return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['year']['value']
        except KeyError:
            return "error"

    def getGasConsumptionFuelCellThisYear(self):
        try:
            return self.service.getProperty('heating.gas.consumption.fuelCell')['properties']['year']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionTotalDays(self):
        try:
            return self.service.getProperty('heating.gas.consumption.total')['properties']['day']['value']
        except KeyError:
            return "error"

    def getGasConsumptionTotalToday(self):
        try:
            return self.service.getProperty('heating.gas.consumption.total')['properties']['day']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionTotalWeeks(self):
        try:
            return self.service.getProperty('heating.gas.consumption.total')['properties']['week']['value']
        except KeyError:
            return "error"

    def getGasConsumptionTotalThisWeek(self):
        try:
            return self.service.getProperty('heating.gas.consumption.total')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionTotalMonths(self):
        try:
            return self.service.getProperty('heating.gas.consumption.total')['properties']['month']['value']
        except KeyError:
            return "error"

    def getGasConsumptionTotalThisMonth(self):
        try:
            return self.service.getProperty('heating.gas.consumption.total')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionTotalYears(self):
        try:
            return self.service.getProperty('heating.gas.consumption.total')['properties']['year']['value']
        except KeyError:
            return "error"

    def getGasConsumptionTotalThisYear(self):
        try:
            return self.service.getProperty('heating.gas.consumption.total')['properties']['year']['value'][0]
        except KeyError:
            return "error"

    def getPowerProductionCoverageTotalDays(self):
        try:
            return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['day']['value']
        except KeyError:
            return "error"

    def getPowerProductionCoverageTotalToday(self):
        try:
            return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['day']['value'][0]
        except KeyError:
            return "error"

    def getPowerProductionCoverageTotalWeeks(self):
        try:
            return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['week']['value']
        except KeyError:
            return "error"

    def getPowerProductionCoverageTotalThisWeek(self):
        try:
            return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getPowerProductionCoverageTotalMonths(self):
        try:
            return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['month']['value']
        except KeyError:
            return "error"

    def getPowerProductionCoverageTotalThisMonth(self):
        try:
            return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getPowerProductionCoverageTotalYears(self):
        try:
            return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['year']['value']
        except KeyError:
            return "error"

    def getPowerProductionCoverageTotalThisYear(self):
        try:
            return self.service.getProperty('heating.power.production.productionCoverage.total')['properties']['year']['value'][0]
        except KeyError:
            return "error"

    def getHeatProductionDays(self):
        try:
            return self.service.getProperty('heating.heat.production')['properties']['day']['value']
        except KeyError:
            return "error"

    def getHeatProductionToday(self):
        try:
            return self.service.getProperty('heating.heat.production')['properties']['day']['value'][0]
        except KeyError:
            return "error"

    def getHeatProductionWeeks(self):
        try:
            return self.service.getProperty('heating.heat.production')['properties']['week']['value']
        except KeyError:
            return "error"

    def getHeatProductionThisWeek(self):
        try:
            return self.service.getProperty('heating.heat.production')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getHeatProductionMonths(self):
        try:
            return self.service.getProperty('heating.heat.production')['properties']['month']['value']
        except KeyError:
            return "error"

    def getHeatProductionThisMonth(self):
        try:
            return self.service.getProperty('heating.heat.production')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getHeatProductionYears(self):
        try:
            return self.service.getProperty('heating.heat.production')['properties']['year']['value']
        except KeyError:
            return "error"

    def getHeatProductionThisYear(self):
        try:
            return self.service.getProperty('heating.heat.production')['properties']['year']['value'][0]
        except KeyError:
            return "error"