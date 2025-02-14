from PyViCare.PyViCareHeatingDevice import HeatingDevice
from PyViCare.PyViCareUtils import handleNotSupported


class PelletsBoiler(HeatingDevice):

    @handleNotSupported
    def getActive(self):
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
        return self.service.getProperty('heating.boiler.airflaps.1.position.current')['properties']['value']['value']

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
    def getFuelUnit(self) -> str:
        return str(self.service.getProperty('heating.configuration.fuel.need')['properties']['value']['unit'])

    @handleNotSupported
    def getBoilerState(self):
        return self.service.getProperty('heating.boiler.operating.phase')['properties']['value']['value']

    @handleNotSupported
    def getBoilerCuircuitPumpStatus(self):
        return self.service.getProperty('heating.boiler.pumps.circuit')['properties']['status']['value']

    @handleNotSupported
    def getBufferMainTemperature(self):
        return self.service.getProperty("heating.bufferCylinder.sensors.temperature.main")["properties"]['value']['value']

    @handleNotSupported
    def getBufferTopTemperature(self):
        return self.service.getProperty("heating.bufferCylinder.sensors.temperature.top")["properties"]['value']['value']

    @handleNotSupported
    def getBufferMidTopTemperature(self):
        return self.service.getProperty("heating.bufferCylinder.sensors.temperature.midTop")["properties"]['value']['value']

    @handleNotSupported
    def getBufferMiddleTemperature(self):
        return self.service.getProperty("heating.bufferCylinder.sensors.temperature.middle")["properties"]['value']['value']

    @handleNotSupported
    def getBufferMidBottomTemperature(self):
        return self.service.getProperty("heating.bufferCylinder.sensors.temperature.midBottom")["properties"]['value']['value']

    @handleNotSupported
    def getBufferBottomTemperature(self):
        return self.service.getProperty("heating.bufferCylinder.sensors.temperature.bottom")["properties"]['value']['value']
