from PyViCare.PyViCareDevice import Device

class GazBoiler(Device):

    def getBurnerActive(self):
        try:
            return self.service.getProperty("heating.burner")["properties"]["active"]["value"]
        except KeyError:
            return "error"

    def getGasConsumptionHeatingDays(self):
        try:
            return self.service.getProperty('heating.gas.consumption.heating')['properties']['day']['value']
        except KeyError:
            return "error"

    def getGasConsumptionHeatingToday(self):
        try:
            return self.service.getProperty('heating.gas.consumption.heating')['properties']['day']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionHeatingWeeks(self):
        try:
            return self.service.getProperty('heating.gas.consumption.heating')['properties']['week']['value']
        except KeyError:
            return "error"

    def getGasConsumptionHeatingThisWeek(self):
        try:
            return self.service.getProperty('heating.gas.consumption.heating')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionHeatingMonths(self):
        try:
            return self.service.getProperty('heating.gas.consumption.heating')['properties']['month']['value']
        except KeyError:
            return "error"

    def getGasConsumptionHeatingThisMonth(self):
        try:
            return self.service.getProperty('heating.gas.consumption.heating')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionHeatingYears(self):
        try:
            return self.service.getProperty('heating.gas.consumption.heating')['properties']['year']['value']
        except KeyError:
            return "error"

    def getGasConsumptionHeatingThisYear(self):
        try:
            return self.service.getProperty('heating.gas.consumption.heating')['properties']['year']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionDomesticHotWaterDays(self):
        try:
            return self.service.getProperty('heating.gas.consumption.dhw')['properties']['day']['value']
        except KeyError:
            return "error"

    def getGasConsumptionDomesticHotWaterToday(self):
        try:
            return self.service.getProperty('heating.gas.consumption.dhw')['properties']['day']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionDomesticHotWaterWeeks(self):
        try:
            return self.service.getProperty('heating.gas.consumption.dhw')['properties']['week']['value']
        except KeyError:
            return "error"

    def getGasConsumptionDomesticHotWaterThisWeek(self):
        try:
            return self.service.getProperty('heating.gas.consumption.dhw')['properties']['week']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionDomesticHotWaterMonths(self):
        try:
            return self.service.getProperty('heating.gas.consumption.dhw')['properties']['month']['value']
        except KeyError:
            return "error"

    def getGasConsumptionDomesticHotWaterThisMonth(self):
        try:
            return self.service.getProperty('heating.gas.consumption.dhw')['properties']['month']['value'][0]
        except KeyError:
            return "error"

    def getGasConsumptionDomesticHotWaterYears(self):
        try:
            return self.service.getProperty('heating.gas.consumption.dhw')['properties']['year']['value']
        except KeyError:
            return "error"

    def getGasConsumptionDomesticHotWaterThisYear(self):
        try:
            return self.service.getProperty('heating.gas.consumption.dhw')['properties']['year']['value'][0]
        except KeyError:
            return "error"
            
    def getBoilerTemperature(self):
        try:
            return self.service.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getCurrentPower(self):
        try:
            return self.service.getProperty('heating.burner.current.power')['properties']['value']['value']
        except KeyError:
            return "error"