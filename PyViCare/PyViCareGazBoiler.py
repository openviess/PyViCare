from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCare import handleKeyError

class GazBoiler(Device):

    @handleKeyError
    def getBurnerActive(self):
        return self.service.getProperty("heating.burner")["properties"]["active"]["value"]

    @handleKeyError
    def getGasConsumptionHeatingDays(self):
        return self.service.getProperty('heating.gas.consumption.heating')['properties']['day']['value']

    @handleKeyError
    def getGasConsumptionHeatingToday(self):
        return self.service.getProperty('heating.gas.consumption.heating')['properties']['day']['value'][0]

    @handleKeyError
    def getGasConsumptionHeatingWeeks(self):
        return self.service.getProperty('heating.gas.consumption.heating')['properties']['week']['value']

    @handleKeyError
    def getGasConsumptionHeatingThisWeek(self):
        return self.service.getProperty('heating.gas.consumption.heating')['properties']['week']['value'][0]

    @handleKeyError
    def getGasConsumptionHeatingMonths(self):
        return self.service.getProperty('heating.gas.consumption.heating')['properties']['month']['value']

    @handleKeyError
    def getGasConsumptionHeatingThisMonth(self):
        return self.service.getProperty('heating.gas.consumption.heating')['properties']['month']['value'][0]

    @handleKeyError
    def getGasConsumptionHeatingYears(self):
        return self.service.getProperty('heating.gas.consumption.heating')['properties']['year']['value']

    @handleKeyError
    def getGasConsumptionHeatingThisYear(self):
        return self.service.getProperty('heating.gas.consumption.heating')['properties']['year']['value'][0]

    @handleKeyError
    def getGasConsumptionDomesticHotWaterDays(self):
        return self.service.getProperty('heating.gas.consumption.dhw')['properties']['day']['value']

    @handleKeyError
    def getGasConsumptionDomesticHotWaterToday(self):
        return self.service.getProperty('heating.gas.consumption.dhw')['properties']['day']['value'][0]

    @handleKeyError
    def getGasConsumptionDomesticHotWaterWeeks(self):
        return self.service.getProperty('heating.gas.consumption.dhw')['properties']['week']['value']

    @handleKeyError
    def getGasConsumptionDomesticHotWaterThisWeek(self):
        return self.service.getProperty('heating.gas.consumption.dhw')['properties']['week']['value'][0]

    @handleKeyError
    def getGasConsumptionDomesticHotWaterMonths(self):
        return self.service.getProperty('heating.gas.consumption.dhw')['properties']['month']['value']

    @handleKeyError
    def getGasConsumptionDomesticHotWaterThisMonth(self):
        return self.service.getProperty('heating.gas.consumption.dhw')['properties']['month']['value'][0]

    @handleKeyError
    def getGasConsumptionDomesticHotWaterYears(self):
        return self.service.getProperty('heating.gas.consumption.dhw')['properties']['year']['value']

    @handleKeyError
    def getGasConsumptionDomesticHotWaterThisYear(self):
        return self.service.getProperty('heating.gas.consumption.dhw')['properties']['year']['value'][0]

            
    @handleKeyError
    def getBurnerModulation(self):
        return self.service.getProperty('heating.burner.modulation')["properties"]["value"]["value"]
            
    @handleKeyError
    def getBoilerTemperature(self):
        return self.service.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]

    @handleKeyError
    def getPowerConsumptionDays(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['day']['value']

    @handleKeyError
    def getPowerConsumptionToday(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['day']['value'][0]

    @handleKeyError
    def getPowerConsumptionWeeks(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['week']['value']

    @handleKeyError
    def getPowerConsumptionThisWeek(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['week']['value'][0]

    @handleKeyError
    def getPowerConsumptionMonths(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['month']['value']

    @handleKeyError
    def getPowerConsumptionThisMonth(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['month']['value'][0]

    @handleKeyError
    def getPowerConsumptionYears(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['year']['value']

    @handleKeyError
    def getPowerConsumptionThisYear(self):
        return self.service.getProperty('heating.power.consumption.total')['properties']['year']['value'][0]

    @handleKeyError
    def getBurnerHours(self):
        return self.service.getProperty('heating.burner.statistics')['properties']['hours']['value']

    @handleKeyError
    def getBurnerStarts(self):
        return self.service.getProperty('heating.burner.statistics')['properties']['starts']['value']

