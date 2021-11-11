from typing import Any, List

from PyViCare.PyViCareDevice import Device, DeviceWithComponent
from PyViCare.PyViCareUtils import handleNotSupported


class PelletsBoiler(Device):
 
    @property
    def burners(self) -> List[Any]:
        return list([self.getBurner(x) for x in self.getAvailableBurners()])



    def getBurner(self, burner):
        return PelletsBoilerBurner(self, burner)

    @handleNotSupported
    def getAvailableBurners(self):
        return self.service.getProperty("heating.burners")["components"]


    @handleNotSupported
    def getActive(self):
        return self.service.getProperty("heating.burner")["properties"]["active"]["value"]

    @handleNotSupported
    def getBurnerModulation(self):
        return self.service.getProperty('heating.burner.modulation')["properties"]["value"]["value"]

    @handleNotSupported
    def getBoilerTemperature(self):
        return self.service.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]

    # @handleNotSupported
    # def getBurnerHours(self):
    #     return self.service.getProperty('heating.burner.statistics')['properties']['hours']['value']

    # @handleNotSupported
    # def getBurnerStarts(self):
    #     return self.service.getProperty('heating.burner.statistics')['properties']['starts']['value']

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



class PelletsBoilerBurner(DeviceWithComponent):



    @property
    def burner(self) -> str:
        return self.component

    @handleNotSupported
    def getActive(self):
        return self.service.getProperty(f"heating.burners.{self.burner}")["properties"]["active"]["value"]

    @handleNotSupported
    def getHours(self):
        return self.service.getProperty(f"heating.burners.{self.burner}.statistics")["properties"]["hours"]["value"]

    @handleNotSupported
    def getStarts(self):
        return self.service.getProperty(f"heating.burners.{self.burner}.statistics")["properties"]["starts"]["value"]

    @handleNotSupported
    def getModulation(self):
        return self.service.getProperty(f"heating.burners.{self.burner}.modulation")["properties"]["value"]["value"]
