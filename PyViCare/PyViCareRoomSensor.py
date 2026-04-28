from __future__ import annotations

from typing import Any, TYPE_CHECKING

from PyViCare.PyViCareDevice import ZigbeeBatteryDevice
from PyViCare.PyViCareUtils import handleNotSupported, handleAPICommandErrors

if TYPE_CHECKING:
    from PyViCare.PyViCareRoomControl import RoomControl


class RoomSensor(ZigbeeBatteryDevice):

    _room_control: RoomControl | None = None
    _room_id: str | None = None

    def setRoomControl(self, room_control: RoomControl, room_id: str) -> None:
        """Enrich this sensor with data from a RoomControl device."""
        self._room_control = room_control
        self._room_id = room_id

    def _getRoomControl(self) -> RoomControl:
        if self._room_control is None:
            raise KeyError("roomControl")
        return self._room_control

    @handleNotSupported
    def getSerial(self) -> Any:
        return self.getProperty("device.sensors.temperature")["deviceId"]

    # --- Sensors (enriched from RoomControl) ---

    @handleNotSupported
    def getTemperature(self) -> Any:
        if self._room_control is not None:
            return self._room_control.getRoomTemperature(self._room_id)
        return self.getProperty("device.sensors.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getHumidity(self) -> Any:
        if self._room_control is not None:
            return self._room_control.getRoomHumidity(self._room_id)
        return self.getProperty("device.sensors.humidity")["properties"]["value"]["value"]

    @handleNotSupported
    def getCO2(self) -> Any:
        return self._getRoomControl().getRoomCO2(self._room_id)

    @handleNotSupported
    def getRoomName(self) -> Any:
        return self._getRoomControl().getRoomName(self._room_id)

    @handleNotSupported
    def getRoomType(self) -> Any:
        return self._getRoomControl().getRoomType(self._room_id)

    @handleNotSupported
    def getCondensationRisk(self) -> Any:
        return self._getRoomControl().getRoomCondensationRisk(self._room_id)

    # --- Operating state ---

    @handleNotSupported
    def getOperatingStateLevel(self) -> Any:
        return self._getRoomControl().getRoomOperatingStateLevel(self._room_id)

    @handleNotSupported
    def getOperatingStateDemand(self) -> Any:
        return self._getRoomControl().getRoomOperatingStateDemand(self._room_id)

    # --- Heating programs ---

    @handleNotSupported
    def getNormalHeatingTemperature(self) -> Any:
        return self._getRoomControl().getRoomNormalHeatingTemperature(self._room_id)

    @handleAPICommandErrors
    def setNormalHeatingTemperature(self, temperature: float) -> None:
        self._getRoomControl().setRoomNormalHeatingTemperature(self._room_id, temperature)

    @handleNotSupported
    def getReducedHeatingTemperature(self) -> Any:
        return self._getRoomControl().getRoomReducedHeatingTemperature(self._room_id)

    @handleAPICommandErrors
    def setReducedHeatingTemperature(self, temperature: float) -> None:
        self._getRoomControl().setRoomReducedHeatingTemperature(self._room_id, temperature)

    @handleNotSupported
    def getComfortHeatingTemperature(self) -> Any:
        return self._getRoomControl().getRoomComfortHeatingTemperature(self._room_id)

    @handleAPICommandErrors
    def setComfortHeatingTemperature(self, temperature: float) -> None:
        self._getRoomControl().setRoomComfortHeatingTemperature(self._room_id, temperature)

    # --- Quick modes ---

    @handleNotSupported
    def getManualTillNextScheduleActive(self) -> Any:
        return self._getRoomControl().getRoomManualTillNextScheduleActive(self._room_id)

    @handleAPICommandErrors
    def activateManualTillNextSchedule(self, temperature: float) -> None:
        self._getRoomControl().activateRoomManualTillNextSchedule(self._room_id, temperature)

    @handleAPICommandErrors
    def deactivateManualTillNextSchedule(self) -> None:
        self._getRoomControl().deactivateRoomManualTillNextSchedule(self._room_id)

    # --- Schedule ---

    @handleNotSupported
    def getSchedule(self) -> Any:
        return self._getRoomControl().getRoomSchedule(self._room_id)
