from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCare import handleKeyError

class OilBoiler(Device):

    @handleKeyError
    def getBurnerActive(self):
        return self.service.getProperty("heating.burner")["properties"]["active"]["value"]

    @handleKeyError         
    def getBurnerModulation(self):
        return self.service.getProperty('heating.burner.modulation')["properties"]["value"]["value"]

    @handleKeyError      
    def getBoilerTemperature(self):
        return self.service.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]

    @handleKeyError
    def getBurnerHours(self):
        return self.service.getProperty('heating.burner.statistics')['properties']['hours']['value']

    @handleKeyError
    def getBurnerStarts(self):
        return self.service.getProperty('heating.burner.statistics')['properties']['starts']['value']
