from contextlib import suppress
from typing import Any, List, Optional

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

    @property
    def leakSensors(self) -> List["LeakSensor"]:
        return [LeakSensor(self, slot) for slot in self.getAvailableLeakSensorSlots()]

    def getAvailableLeakSensorSlots(self) -> List[int]:
        available: List[int] = []
        for slot in range(_LEAK_SENSOR_SLOTS):
            with suppress(PyViCareNotSupportedFeatureError):
                feature = self.getProperty(f"water.leakDetection.sensors.leakage.{slot}")
                if feature.get("isEnabled"):
                    available.append(slot)
        return available

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


class LeakSensor:
    """Single wireless leakage sensor connected to a Vitoset Aqua."""

    def __init__(self, device: WaterTreatment, slot: int) -> None:
        self.service = device.service
        self.slot = slot
        self.device = device

    @property
    def id(self) -> int:
        return self.slot

    def getProperty(self, property_name: str) -> Any:
        return self.device.getProperty(property_name)

    @handleNotSupported
    def getStatus(self) -> str:
        return str(self.getProperty(f"water.leakDetection.sensors.leakage.{self.slot}")["properties"]["status"]["value"])

    @handleNotSupported
    def getLeakDetected(self) -> bool:
        return bool(self.getProperty(f"water.leakDetection.sensors.leakage.{self.slot}")["properties"]["value"]["value"])

    @handleNotSupported
    def getSensorId(self) -> str:
        return str(self.getProperty(f"water.leakDetection.sensors.leakage.{self.slot}.id")["properties"]["value"]["value"])

    @handleNotSupported
    def getName(self) -> str:
        return str(self.getProperty(f"water.leakDetection.sensors.leakage.{self.slot}.name")["properties"]["name"]["value"])

    @handleNotSupported
    def getBatteryPercent(self) -> int:
        return int(self.getProperty(f"water.leakDetection.sensors.leakage.{self.slot}.battery")["properties"]["level"]["value"])

    @handleNotSupported
    def getRssi(self) -> int:
        return int(self.getProperty(f"water.leakDetection.sensors.leakage.{self.slot}.rssi")["properties"]["value"]["value"])

    def getHardwareVersion(self) -> Optional[dict[str, int]]:
        try:
            feature = self.getProperty(f"water.leakDetection.sensors.leakage.{self.slot}.version.hardware")
        except PyViCareNotSupportedFeatureError:
            return None
        return self._versionFields(feature.get("properties") or {})

    def getSoftwareVersion(self) -> Optional[dict[str, int]]:
        try:
            feature = self.getProperty(f"water.leakDetection.sensors.leakage.{self.slot}.version.software")
        except PyViCareNotSupportedFeatureError:
            return None
        return self._versionFields(feature.get("properties") or {})

    @staticmethod
    def _versionFields(props: dict[str, Any]) -> Optional[dict[str, int]]:
        if not props:
            return None
        return {
            field: int(props[field]["value"])
            for field in ("build", "family", "revision", "version")
            if field in props
        }
