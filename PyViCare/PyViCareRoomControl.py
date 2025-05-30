from typing import Any, List

from PyViCare.PyViCareDevice import Device, DeviceWithComponent
from PyViCare.PyViCareUtils import handleNotSupported, handleAPICommandErrors


class RoomControl(Device):

    @property
    def rooms(self) -> List[Any]:
        return list([self.getRoom(x) for x in self.getAvailableRooms()])

    def getRoom(self, room):
        return Room(self, room)

    @handleNotSupported
    def getAvailableRooms(self):
        return self.service.getProperty("rooms")["properties"]["enabled"]["value"]


class Room(DeviceWithComponent):
    @property
    def room(self) -> str:
        return self.component

    @handleNotSupported
    def getType(self):
        return self.service.getProperty(f"rooms.{self.room}")["properties"]["type"]["value"]

    @handleNotSupported
    def getName(self):
        return self.service.getProperty(f"rooms.{self.room}")["properties"]["name"]["value"]

    @property
    def actors(self) -> List[Any]:
        return list([self.getActor(x) for x in self.getAvailableActors()])

    def getActor(self, actor):
        return Actor(self, actor)

    @handleNotSupported
    def getAvailableActors(self):
        return list(map(lambda _: _["deviceId"],
                        self.service.getProperty(f"rooms.{self.room}")["properties"]["actors"]["value"]))

    @handleNotSupported
    def getOperatingStateLevel(self) -> str:
        return str(self.service.getProperty(f"rooms.{self.room}.operating.state")["properties"]["level"]["value"])

    @handleNotSupported
    def getOperatingStateDemand(self) -> str:
        return str(self.service.getProperty(f"rooms.{self.room}.operating.state")["properties"]["demand"]["value"])

    @handleNotSupported
    def getOperatingStateReason(self) -> str:
        return str(self.service.getProperty(f"rooms.{self.room}.operating.state")["properties"]["reason"]["value"])

    @handleNotSupported
    def getOperatingStateModifier(self) -> str:
        return str(self.service.getProperty(f"rooms.{self.room}.operating.state")["properties"]["modifier"]["value"])

    @handleNotSupported
    def getSensorTemperature(self) -> float:
        return float(self.service.getProperty(f"rooms.{self.room}.sensors.temperature")["properties"]["value"]["value"])

    @handleNotSupported
    def getSensorTemperatureStatus(self) -> str:
        return str(self.service.getProperty(f"rooms.{self.room}.sensors.temperature")["properties"]["status"]["value"])

    @handleNotSupported
    def getSensorHumidity(self) -> float:
        return float(self.service.getProperty(f"rooms.{self.room}.sensors.humidity")["properties"]["value"]["value"])

    @handleNotSupported
    def getSensorHumidityStatus(self) -> str:
        return str(self.service.getProperty(f"rooms.{self.room}.sensors.humidity")["properties"]["status"]["value"])

    @handleNotSupported
    def getSensorCO2(self) -> float:
        return float(self.service.getProperty(f"rooms.{self.room}.sensors.co2")["properties"]["value"]["value"])

    @handleNotSupported
    def getSensorCO2Status(self) -> str:
        return str(self.service.getProperty(f"rooms.{self.room}.sensors.co2")["properties"]["status"]["value"])

    @handleNotSupported
    def getNormalHeatingTemperature(self) -> float:
        return float(self.service.getProperty(f"rooms.{self.room}.operating.programs.normalHeating")["properties"][
                         "temperature"]["value"])

    @handleNotSupported
    def getNormalHeatingActive(self) -> bool:
        return bool(
            self.service.getProperty(f"rooms.{self.room}.operating.programs.normalHeating")["properties"]["active"][
                "value"])

    @handleAPICommandErrors
    def setNormalHeatingTemperature(self, temperature: float) -> Any:
        return self.service.setProperty(f"rooms.{self.room}.operating.programs.normalHeating", "setTemperature",
                                        {'targetTemperature': temperature})

    @handleNotSupported
    def getReducedHeatingTemperature(self) -> float:
        return float(self.service.getProperty(f"rooms.{self.room}.operating.programs.reducedHeating")["properties"][
                         "temperature"]["value"])

    @handleNotSupported
    def getReducedHeatingActive(self) -> bool:
        return bool(
            self.service.getProperty(f"rooms.{self.room}.operating.programs.reducedHeating")["properties"]["active"][
                "value"])

    @handleAPICommandErrors
    def setReducedHeatingTemperature(self, temperature: float) -> Any:
        return self.service.setProperty(f"rooms.{self.room}.operating.programs.reducedHeating", "setTemperature",
                                        {'targetTemperature': temperature})

    @handleNotSupported
    def getComfortHeatingTemperature(self) -> float:
        return float(self.service.getProperty(f"rooms.{self.room}.operating.programs.comfortHeating")["properties"][
                         "temperature"]["value"])

    @handleNotSupported
    def getComfortHeatingActive(self) -> bool:
        return bool(
            self.service.getProperty(f"rooms.{self.room}.operating.programs.comfortHeating")["properties"]["active"][
                "value"])

    @handleAPICommandErrors
    def setComfortHeatingTemperature(self, temperature: float) -> Any:
        return self.service.setProperty(f"rooms.{self.room}.operating.programs.comfortHeating", "setTemperature",
                                        {'targetTemperature': temperature})

    @handleNotSupported
    def getNormalCoolingTemperature(self) -> float:
        return float(self.service.getProperty(f"rooms.{self.room}.operating.programs.normalCooling")["properties"][
                         "temperature"]["value"])

    @handleNotSupported
    def getNormalCoolingActive(self) -> bool:
        return bool(
            self.service.getProperty(f"rooms.{self.room}.operating.programs.normalCooling")["properties"]["active"][
                "value"])

    @handleAPICommandErrors
    def setNormalCoolingTemperature(self, temperature: float) -> Any:
        return self.service.setProperty(f"rooms.{self.room}.operating.programs.normalCooling", "setTemperature",
                                        {'targetTemperature': temperature})

    @handleNotSupported
    def getReducedCoolingTemperature(self) -> float:
        return float(self.service.getProperty(f"rooms.{self.room}.operating.programs.reducedCooling")["properties"][
                         "temperature"]["value"])

    @handleNotSupported
    def getReducedCoolingActive(self) -> bool:
        return bool(
            self.service.getProperty(f"rooms.{self.room}.operating.programs.reducedCooling")["properties"]["active"][
                "value"])

    @handleAPICommandErrors
    def setReducedCoolingTemperature(self, temperature: float) -> Any:
        return self.service.setProperty(f"rooms.{self.room}.operating.programs.reducedCooling", "setTemperature",
                                        {'targetTemperature': temperature})

    @handleNotSupported
    def getComfortCoolingTemperature(self) -> float:
        return float(self.service.getProperty(f"rooms.{self.room}.operating.programs.comfortCooling")["properties"][
                         "temperature"]["value"])

    @handleNotSupported
    def getComfortCoolingActive(self) -> bool:
        return bool(
            self.service.getProperty(f"rooms.{self.room}.operating.programs.comfortCooling")["properties"]["active"][
                "value"])

    @handleAPICommandErrors
    def setComfortCoolingTemperature(self, temperature: float) -> Any:
        return self.service.setProperty(f"rooms.{self.room}.operating.programs.comfortCooling", "setTemperature",
                                        {'targetTemperature': temperature})

    @handleNotSupported
    def getSchedule(self):
        properties = self.service.getProperty(
            f"rooms.{self.room}.schedule")["properties"]
        return {
            "active": properties["active"]["value"],
            "mon": properties["entries"]["value"]["mon"],
            "tue": properties["entries"]["value"]["tue"],
            "wed": properties["entries"]["value"]["wed"],
            "thu": properties["entries"]["value"]["thu"],
            "fri": properties["entries"]["value"]["fri"],
            "sat": properties["entries"]["value"]["sat"],
            "sun": properties["entries"]["value"]["sun"]
        }

    # TODO: Set schedule

    @handleNotSupported
    def getManualTillNextScheduleActive(self) -> bool:
        return bool(
            self.service.getProperty(f"rooms.{self.room}.quickmodes.manualTillNextSchedule")["properties"]["active"][
                "value"])

    @handleAPICommandErrors
    def setManualTillNextScheduleTemperature(self, temperature: float) -> Any:
        return self.service.setProperty(f"rooms.{self.room}.quickmodes.manualTillNextSchedule", "setTemperature",
                                        {'targetTemperature': temperature})

    @handleAPICommandErrors
    def activateManualTillNextSchedule(self, temperature: float) -> Any:
        return self.service.setProperty(f"rooms.{self.room}.quickmodes.manualTillNextSchedule", "activate",
                                        {'temperature': temperature})

    @handleAPICommandErrors
    def deactivateManualTillNextSchedule(self) -> Any:
        return self.service.setProperty(f"rooms.{self.room}.quickmodes.manualTillNextSchedule", "deactivate")


class Actor(DeviceWithComponent):
    @property
    def actor(self) -> str:
        return self.component
