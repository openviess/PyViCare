import re
from typing import Any

from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareHeatingDevice import HeatingDeviceWithComponent
from PyViCare.PyViCareUtils import handleNotSupported


class RoomControl(Device):
    """Viessmann RoomControl virtual device.

    Exposes per-room sensor readings, setpoints and configuration flags
    on the public IoT scope. All accessors are read-only; the API does
    not return write commands for room features on this scope.
    """

    @handleNotSupported
    def getAvailableRoomIds(self) -> list[str]:
        """Return the list of room indices for which the API returns data.

        IoT scope no longer exposes a `rooms` parent feature, so we scan
        the full feature list for `rooms.<n>.*` prefixes and report the
        unique numeric indices, sorted numerically. Placeholder slots whose
        features are all disabled are skipped.
        """
        features = self.service.fetch_all_features(self.accessor).get("data", [])
        ids = set()
        pattern = re.compile(r"^rooms\.(\d+)\.")
        for feature in features:
            name = feature.get("feature", "")
            match = pattern.match(name)
            if match and feature.get("isEnabled"):
                ids.add(match.group(1))
        return sorted(ids, key=int)

    @property
    def rooms(self) -> list[Any]:
        return [Room(self, room_id) for room_id in self.getAvailableRoomIds()]

    # --- sensor readings ---

    @handleNotSupported
    def getRoomTemperature(self, room_id: str) -> float:
        return float(self.getProperty(f"rooms.{room_id}.sensors.temperature")["properties"]["value"]["value"])

    @handleNotSupported
    def getRoomHumidity(self, room_id: str) -> float:
        return float(self.getProperty(f"rooms.{room_id}.sensors.humidity")["properties"]["value"]["value"])

    @handleNotSupported
    def getRoomCO2(self, room_id: str) -> int:
        return int(self.getProperty(f"rooms.{room_id}.co2")["properties"]["concentration"]["value"])

    @handleNotSupported
    def getRoomCondensationRisk(self, room_id: str) -> bool:
        return bool(self.getProperty(f"rooms.{room_id}.condensationRisk")["properties"]["value"]["value"])

    # --- temperature setpoints per program-level (°C) ---

    @handleNotSupported
    def getRoomSetpointComfortHeating(self, room_id: str) -> float:
        return float(self.getProperty(f"rooms.{room_id}.temperature.levels.comfort.heating")["properties"]["temperature"]["value"])

    @handleNotSupported
    def getRoomSetpointNormalHeating(self, room_id: str) -> float:
        return float(self.getProperty(f"rooms.{room_id}.temperature.levels.normal.heating")["properties"]["temperature"]["value"])

    @handleNotSupported
    def getRoomSetpointReducedHeating(self, room_id: str) -> float:
        return float(self.getProperty(f"rooms.{room_id}.temperature.levels.reduced.heating")["properties"]["temperature"]["value"])

    @handleNotSupported
    def getRoomSetpointNormalCooling(self, room_id: str) -> float:
        return float(self.getProperty(f"rooms.{room_id}.temperature.levels.normal.cooling")["properties"]["temperature"]["value"])

    @handleNotSupported
    def getRoomSetpointReducedCooling(self, room_id: str) -> float:
        return float(self.getProperty(f"rooms.{room_id}.temperature.levels.reduced.cooling")["properties"]["temperature"]["value"])

    @handleNotSupported
    def getRoomSetpointNormalPerceived(self, room_id: str) -> float:
        return float(self.getProperty(f"rooms.{room_id}.temperature.levels.normal.perceived")["properties"]["temperature"]["value"])

    @handleNotSupported
    def getRoomSetpointComfortPerceived(self, room_id: str) -> float:
        return float(self.getProperty(f"rooms.{room_id}.temperature.levels.comfort.perceived")["properties"]["temperature"]["value"])

    # --- room state flags ---

    @handleNotSupported
    def getRoomChildLockActive(self, room_id: str) -> bool:
        return bool(self.getProperty(f"rooms.{room_id}.childLock")["properties"]["active"]["value"])

    @handleNotSupported
    def getRoomChildLockStatus(self, room_id: str) -> str:
        return str(self.getProperty(f"rooms.{room_id}.childLock")["properties"]["status"]["value"])

    @handleNotSupported
    def getRoomWindowOpen(self, room_id: str) -> bool:
        # Uses the modern `rooms.X.sensors.openWindow` feature; the legacy
        # `rooms.X.sensors.window.openState` path is in the deprecation
        # database (removal date 2024-09-15).
        return bool(self.getProperty(f"rooms.{room_id}.sensors.openWindow")["properties"]["value"]["value"])

    # --- room configuration flags (whether a feature is enabled, not its value) ---

    @handleNotSupported
    def getRoomOpenWindowDetectionEnabled(self, room_id: str) -> bool:
        return bool(self.getProperty(f"rooms.{room_id}.configuration.openWindow")["properties"]["active"]["value"])

    @handleNotSupported
    def getRoomHydraulicBalancingEnabled(self, room_id: str) -> bool:
        return bool(self.getProperty(f"rooms.{room_id}.configuration.hydraulicBalancing")["properties"]["value"]["value"])

    @handleNotSupported
    def getRoomTrvAlgorithmEnabled(self, room_id: str) -> bool:
        return bool(self.getProperty(f"rooms.{room_id}.configuration.trvAlgorithmActive")["properties"]["value"]["value"])

    @handleNotSupported
    def getRoomHeatOnTimeEnabled(self, room_id: str) -> bool:
        return bool(self.getProperty(f"rooms.{room_id}.configuration.heatOnTime")["properties"]["active"]["value"])


class Room(HeatingDeviceWithComponent):
    """One room of a RoomControl device."""

    def __init__(self, device: RoomControl, room_id: str) -> None:
        # The base class only uses service and getProperty, which RoomControl has.
        super().__init__(device, room_id)  # type: ignore[arg-type]
        self.room_control = device

    def getTemperature(self):
        return self.room_control.getRoomTemperature(self.id)

    def getHumidity(self):
        return self.room_control.getRoomHumidity(self.id)

    def getCO2(self):
        return self.room_control.getRoomCO2(self.id)

    def getCondensationRisk(self):
        return self.room_control.getRoomCondensationRisk(self.id)
