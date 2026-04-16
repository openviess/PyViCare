import logging

from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError, handleNotSupported, handleAPICommandErrors

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class RoomControl(Device):
    """Viessmann RoomControl virtual device.

    Aggregates room sensor data and heating programs.
    Used to enrich physical Zigbee devices with room data.
    """

    @handleNotSupported
    def getAvailableRooms(self):
        return self.service.getProperty("rooms")["properties"]["enabled"]["value"]

    def getRoomActorIds(self, room_id):
        """Return list of actor device IDs for a room."""
        try:
            actors = self.service.getProperty(f"rooms.{room_id}")["properties"]["actors"]["value"]
            return [a["deviceId"] for a in actors]
        except (PyViCareNotSupportedFeatureError, KeyError):
            return []

    def getRoomName(self, room_id):
        try:
            return self.service.getProperty(f"rooms.{room_id}")["properties"]["name"]["value"]
        except (PyViCareNotSupportedFeatureError, KeyError):
            return None

    def getRoomType(self, room_id):
        try:
            return self.service.getProperty(f"rooms.{room_id}")["properties"]["type"]["value"]
        except (PyViCareNotSupportedFeatureError, KeyError):
            return None

    # --- Sensors ---

    def getRoomTemperature(self, room_id):
        return self.service.getProperty(f"rooms.{room_id}.sensors.temperature")["properties"]["value"]["value"]

    def getRoomHumidity(self, room_id):
        return self.service.getProperty(f"rooms.{room_id}.sensors.humidity")["properties"]["value"]["value"]

    def getRoomCO2(self, room_id):
        return self.service.getProperty(f"rooms.{room_id}.sensors.co2")["properties"]["value"]["value"]

    def getRoomCondensationRisk(self, room_id):
        return self.service.getProperty(f"rooms.{room_id}.condensationRisk")["properties"]["value"]["value"]

    # --- Operating state ---

    def getRoomOperatingStateLevel(self, room_id):
        return self.service.getProperty(f"rooms.{room_id}.operating.state")["properties"]["level"]["value"]

    def getRoomOperatingStateDemand(self, room_id):
        return self.service.getProperty(f"rooms.{room_id}.operating.state")["properties"]["demand"]["value"]

    def getRoomOperatingStateReason(self, room_id):
        return self.service.getProperty(f"rooms.{room_id}.operating.state")["properties"]["reason"]["value"]

    # --- Heating programs ---

    def getRoomNormalHeatingTemperature(self, room_id):
        return self.service.getProperty(f"rooms.{room_id}.operating.programs.normalHeating")["properties"]["temperature"]["value"]

    @handleAPICommandErrors
    def setRoomNormalHeatingTemperature(self, room_id, temperature):
        return self.service.setProperty(f"rooms.{room_id}.operating.programs.normalHeating", "setTemperature",
                                        {"targetTemperature": temperature})

    def getRoomReducedHeatingTemperature(self, room_id):
        return self.service.getProperty(f"rooms.{room_id}.operating.programs.reducedHeating")["properties"]["temperature"]["value"]

    @handleAPICommandErrors
    def setRoomReducedHeatingTemperature(self, room_id, temperature):
        return self.service.setProperty(f"rooms.{room_id}.operating.programs.reducedHeating", "setTemperature",
                                        {"targetTemperature": temperature})

    def getRoomComfortHeatingTemperature(self, room_id):
        return self.service.getProperty(f"rooms.{room_id}.operating.programs.comfortHeating")["properties"]["temperature"]["value"]

    @handleAPICommandErrors
    def setRoomComfortHeatingTemperature(self, room_id, temperature):
        return self.service.setProperty(f"rooms.{room_id}.operating.programs.comfortHeating", "setTemperature",
                                        {"targetTemperature": temperature})

    # --- Schedule ---

    def getRoomSchedule(self, room_id):
        props = self.service.getProperty(f"rooms.{room_id}.schedule")["properties"]
        return {
            "active": props["active"]["value"],
            "mon": props["entries"]["value"]["mon"],
            "tue": props["entries"]["value"]["tue"],
            "wed": props["entries"]["value"]["wed"],
            "thu": props["entries"]["value"]["thu"],
            "fri": props["entries"]["value"]["fri"],
            "sat": props["entries"]["value"]["sat"],
            "sun": props["entries"]["value"]["sun"],
        }

    # --- Quick modes ---

    def getRoomManualTillNextScheduleActive(self, room_id):
        return self.service.getProperty(
            f"rooms.{room_id}.quickmodes.manualTillNextSchedule")["properties"]["active"]["value"]

    @handleAPICommandErrors
    def activateRoomManualTillNextSchedule(self, room_id, temperature):
        return self.service.setProperty(f"rooms.{room_id}.quickmodes.manualTillNextSchedule", "activate",
                                        {"temperature": temperature})

    @handleAPICommandErrors
    def deactivateRoomManualTillNextSchedule(self, room_id):
        return self.service.setProperty(f"rooms.{room_id}.quickmodes.manualTillNextSchedule", "deactivate", {})

    # --- Mapping ---

    def buildActorRoomMap(self):
        """Build a mapping of actor device ID -> room ID."""
        actor_map = {}
        try:
            rooms = self.getAvailableRooms()
        except PyViCareNotSupportedFeatureError:
            return actor_map

        for room_id in rooms:
            for actor_id in self.getRoomActorIds(room_id):
                actor_map[actor_id] = room_id
        return actor_map
