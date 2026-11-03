from datetime import date, datetime
from typing import Any

from PyViCare.PyViCareEvent import EVENT_TYPE_DEVICE_ERROR, ViCareEvent
from PyViCare.PyViCareService import ViCareDeviceAccessor, ViCareService, hasRoles
from PyViCare.PyViCareUtils import (
    PyViCareNotSupportedFeatureError,
    handleAPICommandErrors,
    handleNotSupported,
)


class Device:
    """This is the base class for all simple devices.
    This class connects to the Viessmann ViCare API.
    The authentication is done through OAuth2.
    Note that currently, a new token is generated for each run.
    """

    def __init__(self, accessor: ViCareDeviceAccessor, service: ViCareService, roles: list[str] | None = None) -> None:
        self.accessor = accessor
        self.service = service
        self.roles = roles if roles is not None else []

    def getProperty(self, property_name: str) -> Any:
        return self.service.getProperty(self.accessor, property_name)

    def setProperty(self, property_name: str, action: str, data: Any) -> Any:
        return self.service.setProperty(self.accessor, property_name, action, data)

    @handleNotSupported
    def getSerial(self):
        return self.getProperty("device.serial")["properties"]["value"]["value"]

    @handleNotSupported
    def getDeviceErrors(self) -> list[Any]:
        return list[Any](self.getProperty("device.messages.errors.raw")["properties"]["entries"]["value"])

    # Power consumption limitation (§14a EnWG):
    @handleNotSupported
    def getPowerConsumptionLimit(self) -> int:
        return int(self.getProperty("device.power.statusReport.consumption")["properties"]["limit"]["value"])

    @handleNotSupported
    def getPowerConsumptionLimitUnit(self) -> str:
        return str(self.getProperty("device.power.statusReport.consumption")["properties"]["limit"]["unit"])

    @handleNotSupported
    def getPowerConsumptionLimitStatus(self) -> str:
        return str(self.getProperty("device.power.statusReport.consumption")["properties"]["status"]["value"])

    @handleNotSupported
    def getPowerConsumptionLimitationSource(self) -> str:
        return str(self.getProperty("device.power.consumption.limitation")["properties"]["value"]["value"])

    # Power production limitation (feed-in):
    @handleNotSupported
    def getPowerProductionLimit(self) -> int:
        return int(self.getProperty("device.power.statusReport.production")["properties"]["limit"]["value"])

    @handleNotSupported
    def getPowerProductionLimitUnit(self) -> str:
        return str(self.getProperty("device.power.statusReport.production")["properties"]["limit"]["unit"])

    @handleNotSupported
    def getPowerProductionLimitStatus(self) -> str:
        return str(self.getProperty("device.power.statusReport.production")["properties"]["status"]["value"])

    def getErrorEvents(self,
                       *,
                       last_days: int | None = None,
                       since: datetime | None = None,
                       on_date: date | None = None,
                       limit: int | None = 10) -> list[ViCareEvent]:
        """Device errors of this device, in the order the API returns them.

        The API is asked for this gateway (`gatewaySerials`) and the page is
        then filtered by device id, so `limit` counts this gateway's events.

        An error comes as two events: `active` is True when it was raised and
        False when it was cleared. For paging and other event types use
        `service.fetch_events()`.
        """
        page = self.service.fetch_events(
            self.accessor, EVENT_TYPE_DEVICE_ERROR,
            last_days=last_days, since=since, on_date=on_date,
            gateway_serials=self.accessor.serial, limit=limit)
        return [event for event in page.events
                if event.device_id == self.accessor.device_id]

    def isLegacyDevice(self) -> bool:
        return hasRoles(["type:legacy"], self.roles)

    def isE3Device(self) -> bool:
        return hasRoles(["type:E3"], self.roles)

    def isDomesticHotWaterDevice(self):
        return self._isTypeDevice("heating.dhw")

    def isSolarThermalDevice(self):
        return self._isTypeDevice("heating.solar")

    def isVentilationDevice(self):
        return self._isTypeDevice("ventilation")

    def _isTypeDevice(self, deviceType: str):
        try:
            return self.getProperty(deviceType)["isEnabled"] and self.getProperty(deviceType)["properties"]["active"]["value"]
        except PyViCareNotSupportedFeatureError:
            return False


class ZigbeeDevice(Device):

    @handleNotSupported
    def getSerial(self) -> str:
        return str(self.getProperty("device.zigbee.parent.id")["deviceId"])

    @handleNotSupported
    def getZigbeeParentID(self) -> str:
        return str(self.getProperty("device.zigbee.parent.id")["properties"]["value"]["value"])

    @handleNotSupported
    def getZigbeeSignalStrength(self) -> int:
        return int(self.getProperty("device.zigbee.lqi")["properties"]["strength"]["value"])

    @handleNotSupported
    def getName(self) -> str:
        return str(self.getProperty("device.name")["properties"]["name"]["value"])

    @handleAPICommandErrors
    def setName(self, name: str) -> None:
        self.setProperty("device.name", "setName", {'name': name})

    @handleNotSupported
    def getIdentification(self) -> bool:
        return bool(self.getProperty("device.identification")["properties"]["triggered"]["value"])

class ZigbeeBatteryDevice(ZigbeeDevice):

    @handleNotSupported
    def getBatteryLevel(self) -> int:
        return int(self.getProperty("device.power.battery")["properties"]["level"]["value"])
