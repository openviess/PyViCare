from typing import Any, List

from PyViCare.PyViCareHeatingDevice import (HeatingDevice,
                                            HeatingDeviceWithComponent,
                                            get_available_burners)
from PyViCare.PyViCareUtils import handleNotSupported


class OilBoiler(HeatingDevice):

    @property
    def burners(self) -> List[Any]:
        return list([self.getBurner(x) for x in self.getAvailableBurners()])

    def getBurner(self, burner):
        return OilBurner(self, burner)

    @handleNotSupported
    def getAvailableBurners(self):
        return get_available_burners(self.service)

    @handleNotSupported
    def getBoilerTemperature(self):
        return self.service.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]


class OilBurner(HeatingDeviceWithComponent):

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
