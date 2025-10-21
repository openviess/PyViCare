from __future__ import annotations
from typing import List

from PyViCare.PyViCareHeatingDevice import (HeatingDevice, HeatingDeviceWithComponent, get_available_burners)
from PyViCare.PyViCareUtils import handleNotSupported


class PelletsBoiler(HeatingDevice):

    @property
    def burners(self) -> List[PelletsBurner]:
        return list([self.getBurner(x) for x in self.getAvailableBurners()])

    def getBurner(self, burner) -> PelletsBurner:
        return PelletsBurner(self, burner)

    @handleNotSupported
    def getAvailableBurners(self):
        return get_available_burners(self.service)

    @handleNotSupported
    def getBoilerTemperature(self):
        return self.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]

    @handleNotSupported
    def getAshLevel(self):
        return self.getProperty('heating.boiler.ash.level.current')['properties']['value']['value']

    @handleNotSupported
    def getAirFlapsPrimaryPosition(self):
        return self.getProperty('heating.boiler.airflaps.0.position.current')['properties']['value']['value']

    @handleNotSupported
    def getAirFlapsSecondaryPosition(self):
        return self.getProperty('heating.boiler.airflaps.1.position.current')['properties']['value']['value']

    @handleNotSupported
    def getExhaustO2Level(self):
        return self.getProperty('heating.flue.sensors.o2.lambda')['properties']['value']['value']

    @handleNotSupported
    def getBoilerCuircuitPumpCurrentLevel(self):
        return self.getProperty('heating.boiler.pumps.circuit.power.current')['properties']['value']['value']

    @handleNotSupported
    def getBoilerReturnTemperature(self):
        return self.getProperty('heating.sensors.temperature.return')['properties']['value']['value']

    @handleNotSupported
    def getFlueTemperature(self):
        return self.getProperty('heating.flue.sensors.temperature.main')['properties']['value']['value']

    @handleNotSupported
    def getFuelNeed(self):
        return self.getProperty('heating.configuration.fuel.need')['properties']['value']['value']

    @handleNotSupported
    def getFuelUnit(self) -> str:
        return str(self.getProperty('heating.configuration.fuel.need')['properties']['value']['unit'])

    @handleNotSupported
    def getBoilerState(self):
        return self.getProperty('heating.boiler.operating.phase')['properties']['value']['value']

    @handleNotSupported
    def getBoilerCuircuitPumpStatus(self):
        return self.getProperty('heating.boiler.pumps.circuit')['properties']['status']['value']
    @handleNotSupported
    def getBufferMainTemperature(self):
        return self.getProperty("heating.bufferCylinder.sensors.temperature.main")["properties"]['value']['value']

    @handleNotSupported
    def getBufferTopTemperature(self):
        return self.getProperty("heating.bufferCylinder.sensors.temperature.top")["properties"]['value']['value']

    @handleNotSupported
    def getBufferMidTopTemperature(self):
        return self.getProperty("heating.bufferCylinder.sensors.temperature.midTop")["properties"]['value']['value']

    @handleNotSupported
    def getBufferMiddleTemperature(self):
        return self.getProperty("heating.bufferCylinder.sensors.temperature.middle")["properties"]['value']['value']

    @handleNotSupported
    def getBufferMidBottomTemperature(self):
        return self.getProperty("heating.bufferCylinder.sensors.temperature.midBottom")["properties"]['value']['value']

    @handleNotSupported
    def getBufferBottomTemperature(self):
        return self.getProperty("heating.bufferCylinder.sensors.temperature.bottom")["properties"]['value']['value']

class PelletsBurner(HeatingDeviceWithComponent):

    @property
    def burner(self) -> str:
        return self.component

    @handleNotSupported
    def getActive(self) -> bool:
        return bool(self.getProperty(f"heating.burners.{self.burner}")["properties"]["active"]["value"])

    @handleNotSupported
    def getHours(self) -> float:
        return float(self.getProperty(f"heating.burners.{self.burner}.statistics")["properties"]["hours"]["value"])

    @handleNotSupported
    def getStarts(self) -> int:
        return int(self.getProperty(f"heating.burners.{self.burner}.statistics")["properties"]["starts"]["value"])
