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

    def _getRoomContext(self) -> tuple[RoomControl, str]:
        """Return (room_control, room_id), raising if not enriched."""
        if self._room_control is None or self._room_id is None:
            raise KeyError("roomControl")
        return self._room_control, self._room_id

    @handleNotSupported
    def getSerial(self) -> str:
        return str(self.getProperty("device.sensors.temperature")["deviceId"])

    # --- Sensors (enriched from RoomControl) ---

    @handleNotSupported
    def getTemperature(self) -> float:
        if self._room_control is not None and self._room_id is not None:
            return self._room_control.getRoomTemperature(self._room_id)
        return float(self.getProperty("device.sensors.temperature")["properties"]["value"]["value"])

    @handleNotSupported
    def getHumidity(self) -> float:
        if self._room_control is not None and self._room_id is not None:
            return self._room_control.getRoomHumidity(self._room_id)
        return float(self.getProperty("device.sensors.humidity")["properties"]["value"]["value"])

    @handleNotSupported
    def getCO2(self) -> int:
        rc, rid = self._getRoomContext()
        return rc.getRoomCO2(rid)

    @handleNotSupported
    def getRoomName(self) -> str | None:
        rc, rid = self._getRoomContext()
        return rc.getRoomName(rid)

    @handleNotSupported
    def getRoomType(self) -> str | None:
        rc, rid = self._getRoomContext()
        return rc.getRoomType(rid)

    @handleNotSupported
    def getCondensationRisk(self) -> bool:
        rc, rid = self._getRoomContext()
        return rc.getRoomCondensationRisk(rid)

    # --- Operating state ---

    @handleNotSupported
    def getOperatingStateLevel(self) -> str:
        rc, rid = self._getRoomContext()
        return rc.getRoomOperatingStateLevel(rid)

    @handleNotSupported
    def getOperatingStateDemand(self) -> str:
        rc, rid = self._getRoomContext()
        return rc.getRoomOperatingStateDemand(rid)

    # --- Heating programs ---

    @handleNotSupported
    def getNormalHeatingTemperature(self) -> float:
        rc, rid = self._getRoomContext()
        return rc.getRoomNormalHeatingTemperature(rid)

    @handleAPICommandErrors
    def setNormalHeatingTemperature(self, temperature: float) -> None:
        rc, rid = self._getRoomContext()
        rc.setRoomNormalHeatingTemperature(rid, temperature)

    @handleNotSupported
    def getReducedHeatingTemperature(self) -> float:
        rc, rid = self._getRoomContext()
        return rc.getRoomReducedHeatingTemperature(rid)

    @handleAPICommandErrors
    def setReducedHeatingTemperature(self, temperature: float) -> None:
        rc, rid = self._getRoomContext()
        rc.setRoomReducedHeatingTemperature(rid, temperature)

    @handleNotSupported
    def getComfortHeatingTemperature(self) -> float:
        rc, rid = self._getRoomContext()
        return rc.getRoomComfortHeatingTemperature(rid)

    @handleAPICommandErrors
    def setComfortHeatingTemperature(self, temperature: float) -> None:
        rc, rid = self._getRoomContext()
        rc.setRoomComfortHeatingTemperature(rid, temperature)

    # --- Quick modes ---

    @handleNotSupported
    def getManualTillNextScheduleActive(self) -> bool:
        rc, rid = self._getRoomContext()
        return rc.getRoomManualTillNextScheduleActive(rid)

    @handleAPICommandErrors
    def activateManualTillNextSchedule(self, temperature: float) -> None:
        rc, rid = self._getRoomContext()
        rc.activateRoomManualTillNextSchedule(rid, temperature)

    @handleAPICommandErrors
    def deactivateManualTillNextSchedule(self) -> None:
        rc, rid = self._getRoomContext()
        rc.deactivateRoomManualTillNextSchedule(rid)

    # --- Schedule ---

    @handleNotSupported
    def getSchedule(self) -> dict[str, Any]:
        rc, rid = self._getRoomContext()
        return rc.getRoomSchedule(rid)
