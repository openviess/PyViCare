import json

from PyViCare.PyViCare import handleNotSupported
from PyViCare.PyViCareDevice import Device


class GazBoiler(Device):

    def getAllProperties(self, cached=False):
        if cached:
            try:
                with open("ViCareData.json","r") as f:
                    data = f.read()
            except:
                self.all_properties = self.service.getProperties()
                data = json.dumps(self.all_properties, indent=4)
                with open('ViCareData.json', 'w') as f:
                    f.write(data)
        else:
            self.all_properties = self.service.getProperties()

    def getProperty(self, property_name):
        for entry in self.all_properties['entities']:
            for classname in entry['class']:
                if classname == property_name:
                    return entry

    @handleNotSupported
    def getBurnerActive(self):
        return 'on' if self.getProperty("heating.burner")["properties"]["active"]["value"] else 'off'

    @handleNotSupported
    def getGasConsumptionHeatingDays(self):
        return self.getProperty('heating.gas.consumption.heating')['properties']['day']['value']

    @handleNotSupported
    def getGasConsumptionHeatingToday(self):
        return self.getProperty('heating.gas.consumption.heating')['properties']['day']['value'][0]

    @handleNotSupported
    def getGasConsumptionHeatingWeeks(self):
        return self.getProperty('heating.gas.consumption.heating')['properties']['week']['value']

    @handleNotSupported
    def getGasConsumptionHeatingThisWeek(self):
        return self.getProperty('heating.gas.consumption.heating')['properties']['week']['value'][0]

    @handleNotSupported
    def getGasConsumptionHeatingMonths(self):
        return self.getProperty('heating.gas.consumption.heating')['properties']['month']['value']

    @handleNotSupported
    def getGasConsumptionHeatingThisMonth(self):
        return self.getProperty('heating.gas.consumption.heating')['properties']['month']['value'][0]

    @handleNotSupported
    def getGasConsumptionHeatingYears(self):
        return self.getProperty('heating.gas.consumption.heating')['properties']['year']['value']

    @handleNotSupported
    def getGasConsumptionHeatingThisYear(self):
        return self.getProperty('heating.gas.consumption.heating')['properties']['year']['value'][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterDays(self):
        return self.getProperty('heating.gas.consumption.dhw')['properties']['day']['value']

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterToday(self):
        return self.getProperty('heating.gas.consumption.dhw')['properties']['day']['value'][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterWeeks(self):
        return self.getProperty('heating.gas.consumption.dhw')['properties']['week']['value']

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterThisWeek(self):
        return self.getProperty('heating.gas.consumption.dhw')['properties']['week']['value'][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterMonths(self):
        return self.getProperty('heating.gas.consumption.dhw')['properties']['month']['value']

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterThisMonth(self):
        return self.getProperty('heating.gas.consumption.dhw')['properties']['month']['value'][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterYears(self):
        return self.getProperty('heating.gas.consumption.dhw')['properties']['year']['value']

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterThisYear(self):
        return self.getProperty('heating.gas.consumption.dhw')['properties']['year']['value'][0]

    @handleNotSupported
    def getBurnerModulation(self):
        return self.getProperty('heating.burner.modulation')["properties"]["value"]["value"]

    @handleNotSupported
    def getBoilerTemperature(self):
        return self.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]

    @handleNotSupported
    def getPowerConsumptionDays(self):
        return self.getProperty('heating.power.consumption.total')['properties']['day']['value']

    @handleNotSupported
    def getPowerConsumptionToday(self):
        return self.getProperty('heating.power.consumption.total')['properties']['day']['value'][0]

    @handleNotSupported
    def getPowerConsumptionWeeks(self):
        return self.getProperty('heating.power.consumption.total')['properties']['week']['value']

    @handleNotSupported
    def getPowerConsumptionThisWeek(self):
        return self.getProperty('heating.power.consumption.total')['properties']['week']['value'][0]

    @handleNotSupported
    def getPowerConsumptionMonths(self):
        return self.getProperty('heating.power.consumption.total')['properties']['month']['value']

    @handleNotSupported
    def getPowerConsumptionThisMonth(self):
        return self.getProperty('heating.power.consumption.total')['properties']['month']['value'][0]

    @handleNotSupported
    def getPowerConsumptionYears(self):
        return self.getProperty('heating.power.consumption.total')['properties']['year']['value']

    @handleNotSupported
    def getPowerConsumptionThisYear(self):
        return self.getProperty('heating.power.consumption.total')['properties']['year']['value'][0]

    @handleNotSupported
    def getBurnerHours(self):
        return self.getProperty('heating.burner.statistics')['properties']['hours']['value']

    @handleNotSupported
    def getBurnerStarts(self):
        return self.getProperty('heating.burner.statistics')['properties']['starts']['value']

    @handleNotSupported
    def getOneTimeCharge(self):
        return self.getProperty('heating.dhw.oneTimeCharge')["properties"]["active"]["value"]

    def deactivateOneTimeCharge(self):
        return self.service.setProperty("heating.dhw.oneTimeCharge", "deactivate", "{}")

    def activateOneTimeCharge(self):
        return self.service.setProperty("heating.dhw.oneTimeCharge", "activate", "{}")
