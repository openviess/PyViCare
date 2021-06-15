from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCare import handleNotSupported


class OilBoiler(Device):

    @handleNotSupported
    def getBurnerActive(self):
        return self.getProperty("heating.burner")["properties"]["active"]["value"]

    @handleNotSupported
    def getBurnerModulation(self):
        return self.getProperty('heating.burner.modulation')["properties"]["value"]["value"]

    @handleNotSupported
    def getBoilerTemperature(self):
        return self.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]

    @handleNotSupported
    def getBurnerHours(self):
        return self.getProperty('heating.burner.statistics')['properties']['hours']['value']

    @handleNotSupported
    def getBurnerStarts(self):
        return self.getProperty('heating.burner.statistics')['properties']['starts']['value']
