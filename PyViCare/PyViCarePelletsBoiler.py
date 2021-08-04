from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleNotSupported


class PelletsBoiler(Device):

    @handleNotSupported
    def getBurnerActive(self):
        return self.service.getProperty("heating.burner")["properties"]["active"]["value"]

    @handleNotSupported
    def getBurnerModulation(self):
        return self.service.getProperty('heating.burner.modulation')["properties"]["value"]["value"]

    @handleNotSupported
    def getBoilerTemperature(self):
        return self.service.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]

    @handleNotSupported
    def getBurnerHours(self):
        return self.service.getProperty('heating.burner.statistics')['properties']['hours']['value']

    @handleNotSupported
    def getBurnerStarts(self):
        return self.service.getProperty('heating.burner.statistics')['properties']['starts']['value']

    @handleNotSupported
    def getAshLevel(self):
        return self.service.getProperty('heating.boiler.ash.level.current')['properties']['value']['value']

    @handleNotSupported
    def getAirFlapsPrimaryPosition(self):
        return self.service.getProperty('heating.boiler.airflaps.0.position.current')['properties']['value']['value']

    @handleNotSupported
    def getAirFlapsSecondaryPosition(self):
        return self.service.getProperty('heating.boiler.airflaps.0.position.current')['properties']['value']['value']

    @handleNotSupported
    def getExhaustO2Level(self):
        return self.service.getProperty('heating.flue.sensors.o2.lambda')['properties']['value']['value']

    @handleNotSupported
    def getBoilerCuircuitPumpCurrentLevel(self):
        return self.service.getProperty('heating.boiler.pumps.circuit.power.current')['properties']['value']['value']

    @handleNotSupported
    def getBoilerReturnTemperature(self):
        return self.service.getProperty('heating.sensors.temperature.return')['properties']['value']['value']

    @handleNotSupported
    def getFlueTemperature(self):
        return self.service.getProperty('heating.flue.sensors.temperature.main')['properties']['value']['value']

    @handleNotSupported
    def getFuelNeed(self):
        return self.service.getProperty('heating.configuration.fuel.need')['properties']['value']['value']

    @handleNotSupported
    def getBoilerState(self):
        return self.service.getProperty('heating.boiler.operating.phase')['properties']['value']['value']

    @handleNotSupported
    def getBoilerCuircuitPumpStatus(self):
        return self.service.getProperty('heating.boiler.pumps.circuit')['properties']['status']['value']
