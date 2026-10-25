from datetime import datetime
from typing import Any

from PyViCare.PyViCareEvent import (
    EVENT_TYPE_DEVICE_ERROR,
    ViCareEvent,
    ViCareEventPage,
)
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

    def getEventPage(self,
                     event_type: str | None = None,
                     since: datetime | str | None = None,
                     until: datetime | str | None = None,
                     limit: int | None = 10,
                     cursor: str | None = None) -> ViCareEventPage:
        """One page of the installation's event history.

        The page holds the events of every device on every gateway. Use
        `getEvents` for this device only.
        """
        return self.service.fetch_events(self.accessor, event_type, since, until, limit, cursor)

    def getEvents(self,
                  event_type: str | None = None,
                  since: datetime | str | None = None,
                  until: datetime | str | None = None,
                  limit: int | None = 10,
                  cursor: str | None = None) -> list[ViCareEvent]:
        """Events of this device, newest first.

        `limit` applies before the device filter, so fewer events come back
        when other devices have events in the same page.
        """
        page = self.getEventPage(event_type, since, until, limit, cursor)
        return [event for event in page.events if event.device_id == self.accessor.device_id]

    def getErrorEvents(self,
                       since: datetime | str | None = None,
                       until: datetime | str | None = None,
                       limit: int | None = 10,
                       cursor: str | None = None) -> list[ViCareEvent]:
        """Device errors of this device, newest first.

        An error comes as two events: `active` is True when it was raised and
        False when it was cleared.
        """
        return self.getEvents(EVENT_TYPE_DEVICE_ERROR, since, until, limit, cursor)

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
