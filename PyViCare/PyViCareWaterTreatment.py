from typing import Any

from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError, handleNotSupported


_LEAK_SENSOR_SLOTS = 5


class WaterTreatment(Device):
    """Viessmann Vitoset Aqua water treatment station.

    Combines water softener, leak detection (up to 5 sensors), consumption metering
    and main shutoff valve in one device.
    """

    # --- Softener ---

    @handleNotSupported
    def getSaltDaysRemaining(self) -> int:
        return int(self.getProperty("water.softener.salt.level.days")["properties"]["remaining"]["value"])

    @handleNotSupported
    def getLowSaltAlertDays(self) -> int:
        return int(self.getProperty("water.softener.configuration.lowSaltAlert")["properties"]["lowLevelAlertDays"]["value"])

    # --- Consumption ---

    @handleNotSupported
    def getCurrentFlow(self) -> float:
        return float(self.getProperty("water.consumption.flow.current")["properties"]["value"]["value"])

    @handleNotSupported
    def getMaxFlow(self) -> float:
        return float(self.getProperty("water.consumption.flow.max")["properties"]["value"]["value"])

    @handleNotSupported
    def getTotalConsumption(self) -> int:
        return int(self.getProperty("water.consumption.summary")["properties"]["total"]["value"])

    # --- Leak Detection ---

    def getLeakSensors(self) -> list[dict[str, Any]]:
        """Return all connected leak sensors.

        Each Vitoset Aqua exposes 5 sensor slots; only slots that report data
        are returned.
        """
        sensors: list[dict[str, Any]] = []
        for slot in range(_LEAK_SENSOR_SLOTS):
            base = self._readProperties(f"water.leakDetection.sensors.leakage.{slot}")
            if not base:
                continue
            id_props = self._readProperties(f"water.leakDetection.sensors.leakage.{slot}.id")
            name_props = self._readProperties(f"water.leakDetection.sensors.leakage.{slot}.name")
            battery_props = self._readProperties(f"water.leakDetection.sensors.leakage.{slot}.battery")
            rssi_props = self._readProperties(f"water.leakDetection.sensors.leakage.{slot}.rssi")
            hw_props = self._readProperties(f"water.leakDetection.sensors.leakage.{slot}.version.hardware")
            sw_props = self._readProperties(f"water.leakDetection.sensors.leakage.{slot}.version.software")
            sensors.append({
                "slot": slot,
                "status": base.get("status", {}).get("value"),
                "leak_detected": base.get("value", {}).get("value"),
                "id": id_props.get("value", {}).get("value"),
                "name": name_props.get("name", {}).get("value"),
                "battery_percent": battery_props.get("level", {}).get("value"),
                "rssi_dbm": rssi_props.get("value", {}).get("value"),
                "hardware_version": _versionDict(hw_props),
                "software_version": _versionDict(sw_props),
            })
        return sensors

    def _readProperties(self, feature: str) -> dict[str, Any]:
        try:
            data = self.getProperty(feature)
        except PyViCareNotSupportedFeatureError:
            return {}
        return data.get("properties") or {}

    @handleNotSupported
    def getFlowAlertMaxDuration(self) -> int:
        return int(self.getProperty("water.leakDetection.configuration.flowAlert")["properties"]["maxDuration"]["value"])

    @handleNotSupported
    def getFlowAlertMaxFlow(self) -> float:
        return float(self.getProperty("water.leakDetection.configuration.flowAlert")["properties"]["maxFlow"]["value"])

    # --- Shutoff Valve ---

    @handleNotSupported
    def getShutoffPosition(self) -> str:
        return str(self.getProperty("water.valves.shutoff.position")["properties"]["value"]["value"])

    @handleNotSupported
    def getShutoffMotorState(self) -> str:
        return str(self.getProperty("water.valves.shutoff.motor")["properties"]["state"]["value"])

    @handleNotSupported
    def getHolidayModeActive(self) -> bool:
        return bool(self.getProperty("water.valves.shutoff.holiday")["properties"]["active"]["value"])


def _versionDict(props: dict[str, Any]) -> dict[str, int] | None:
    if not props:
        return None
    return {
        field: int(props[field]["value"])
        for field in ("build", "family", "revision", "version")
        if field in props
    }
