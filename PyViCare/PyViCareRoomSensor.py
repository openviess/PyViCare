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

    def _getRoomControl(self):
        if self._room_control is None:
            raise KeyError("roomControl")
        return self._room_control

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
        return self._getRoomControl().getRoomCO2(self._room_id)

    @handleNotSupported
    def getRoomName(self):
        return self._getRoomControl().getRoomName(self._room_id)

    @handleNotSupported
    def getRoomType(self):
        return self._getRoomControl().getRoomType(self._room_id)

    @handleNotSupported
    def getCondensationRisk(self):
        return self._getRoomControl().getRoomCondensationRisk(self._room_id)

    # --- Operating state ---

    @handleNotSupported
    def getOperatingStateLevel(self):
        return self._getRoomControl().getRoomOperatingStateLevel(self._room_id)

    @handleNotSupported
    def getOperatingStateDemand(self):
        return self._getRoomControl().getRoomOperatingStateDemand(self._room_id)

    # --- Heating programs ---

    @handleNotSupported
    def getNormalHeatingTemperature(self):
        return self._getRoomControl().getRoomNormalHeatingTemperature(self._room_id)

    @handleAPICommandErrors
    def setNormalHeatingTemperature(self, temperature):
        return self._getRoomControl().setRoomNormalHeatingTemperature(self._room_id, temperature)

    @handleNotSupported
    def getReducedHeatingTemperature(self):
        return self._getRoomControl().getRoomReducedHeatingTemperature(self._room_id)

    @handleAPICommandErrors
    def setReducedHeatingTemperature(self, temperature):
        return self._getRoomControl().setRoomReducedHeatingTemperature(self._room_id, temperature)

    @handleNotSupported
    def getComfortHeatingTemperature(self):
        return self._getRoomControl().getRoomComfortHeatingTemperature(self._room_id)

    @handleAPICommandErrors
    def setComfortHeatingTemperature(self, temperature):
        return self._getRoomControl().setRoomComfortHeatingTemperature(self._room_id, temperature)

    # --- Quick modes ---

    @handleNotSupported
    def getManualTillNextScheduleActive(self):
        return self._getRoomControl().getRoomManualTillNextScheduleActive(self._room_id)

    @handleAPICommandErrors
    def activateManualTillNextSchedule(self, temperature):
        return self._getRoomControl().activateRoomManualTillNextSchedule(self._room_id, temperature)

    @handleAPICommandErrors
    def deactivateManualTillNextSchedule(self):
        return self._getRoomControl().deactivateRoomManualTillNextSchedule(self._room_id)

    # --- Schedule ---

    @handleNotSupported
    def getSchedule(self):
        return self._getRoomControl().getRoomSchedule(self._room_id)
