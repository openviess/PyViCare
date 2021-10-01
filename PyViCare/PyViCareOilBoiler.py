from typing import Any, List

from PyViCare.PyViCareDevice import Device, DeviceWithComponent
from PyViCare.PyViCareUtils import handleNotSupported


class OilBoiler(Device):

    @property
    def burners(self) -> List[Any]:
        return list([self.getBurner(x) for x in self.getAvailableBurners()])

    def getBurner(self, burner):
        return OilBurner(self, burner)

    @handleNotSupported
    def getAvailableBurners(self):
        return self.service.getProperty("heating.burners")["components"]

    @handleNotSupported
    def getBoilerTemperature(self):
        return self.service.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]


class OilBurner(DeviceWithComponent):

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
