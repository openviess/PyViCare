from PyViCare.PyViCareDevice import ZigbeeBatteryDevice
from PyViCare.PyViCareUtils import handleNotSupported, handleAPICommandErrors


class RoomSensor(ZigbeeBatteryDevice):

    def __init__(self, service):
        super().__init__(service)
        self._room_control = None
        self._room_id = None

    def setRoomControl(self, room_control, room_id):
        """Enrich this sensor with data from a RoomControl device."""
        self._room_control = room_control
        self._room_id = room_id

    @handleNotSupported
    def getSerial(self):
        return self.getProperty("device.sensors.temperature")["deviceId"]

    # --- Sensors (enriched from RoomControl) ---

    @handleNotSupported
    def getTemperature(self):
        if self._room_control is not None:
            return self._room_control.getRoomTemperature(self._room_id)
        return self.getProperty("device.sensors.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getHumidity(self):
        if self._room_control is not None:
            return self._room_control.getRoomHumidity(self._room_id)
        return self.getProperty("device.sensors.humidity")["properties"]["value"]["value"]

    @handleNotSupported
    def getCO2(self):
        if self._room_control is not None:
            return self._room_control.getRoomCO2(self._room_id)
        return None

    @handleNotSupported
    def getRoomName(self):
        if self._room_control is not None:
            return self._room_control.getRoomName(self._room_id)
        return None

    @handleNotSupported
    def getRoomType(self):
        if self._room_control is not None:
            return self._room_control.getRoomType(self._room_id)
        return None

    @handleNotSupported
    def getCondensationRisk(self):
        if self._room_control is not None:
            return self._room_control.getRoomCondensationRisk(self._room_id)
        return None

    # --- Operating state ---

    @handleNotSupported
    def getOperatingStateLevel(self):
        if self._room_control is not None:
            return self._room_control.getRoomOperatingStateLevel(self._room_id)
        return None

    @handleNotSupported
    def getOperatingStateDemand(self):
        if self._room_control is not None:
            return self._room_control.getRoomOperatingStateDemand(self._room_id)
        return None

    # --- Heating programs ---

    @handleNotSupported
    def getNormalHeatingTemperature(self):
        if self._room_control is not None:
            return self._room_control.getRoomNormalHeatingTemperature(self._room_id)
        return None

    @handleAPICommandErrors
    def setNormalHeatingTemperature(self, temperature):
        if self._room_control is not None:
            return self._room_control.setRoomNormalHeatingTemperature(self._room_id, temperature)

    @handleNotSupported
    def getReducedHeatingTemperature(self):
        if self._room_control is not None:
            return self._room_control.getRoomReducedHeatingTemperature(self._room_id)
        return None

    @handleAPICommandErrors
    def setReducedHeatingTemperature(self, temperature):
        if self._room_control is not None:
            return self._room_control.setRoomReducedHeatingTemperature(self._room_id, temperature)

    @handleNotSupported
    def getComfortHeatingTemperature(self):
        if self._room_control is not None:
            return self._room_control.getRoomComfortHeatingTemperature(self._room_id)
        return None

    @handleAPICommandErrors
    def setComfortHeatingTemperature(self, temperature):
        if self._room_control is not None:
            return self._room_control.setRoomComfortHeatingTemperature(self._room_id, temperature)

    # --- Quick modes ---

    @handleNotSupported
    def getManualTillNextScheduleActive(self):
        if self._room_control is not None:
            return self._room_control.getRoomManualTillNextScheduleActive(self._room_id)
        return None

    @handleAPICommandErrors
    def activateManualTillNextSchedule(self, temperature):
        if self._room_control is not None:
            return self._room_control.activateRoomManualTillNextSchedule(self._room_id, temperature)

    @handleAPICommandErrors
    def deactivateManualTillNextSchedule(self):
        if self._room_control is not None:
            return self._room_control.deactivateRoomManualTillNextSchedule(self._room_id)

    # --- Schedule ---

    @handleNotSupported
    def getSchedule(self):
        if self._room_control is not None:
            return self._room_control.getRoomSchedule(self._room_id)
        return None
