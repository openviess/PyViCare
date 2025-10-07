from typing import Any

from PyViCare.PyViCareService import ViCareService
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError, handleAPICommandErrors, handleNotSupported


class Device:
    """This is the base class for all simple devices.
    This class connects to the Viessmann ViCare API.
    The authentication is done through OAuth2.
    Note that currently, a new token is generated for each run.
    """

    def __init__(self, service: ViCareService) -> None:
        self.service = service

    @handleNotSupported
    def getSerial(self):
        return self.service.getProperty("device.serial")["properties"]["value"]["value"]

    @handleNotSupported
    def getDeviceErrors(self) -> list[Any]:
        return list[Any](self.service.getProperty("device.messages.errors.raw")["properties"]["entries"]["value"])

    def isLegacyDevice(self) -> bool:
        return self.service.hasRoles(["type:legacy"])

    def isE3Device(self) -> bool:
        return self.service.hasRoles(["type:E3"])

    def isDomesticHotWaterDevice(self):
        return self._isTypeDevice("heating.dhw")

    def isSolarThermalDevice(self):
        return self._isTypeDevice("heating.solar")

    def isVentilationDevice(self):
        return self._isTypeDevice("ventilation")

    def _isTypeDevice(self, deviceType: str):
        try:
            return self.service.getProperty(deviceType)["isEnabled"] and self.service.getProperty(deviceType)["properties"]["active"]["value"]
        except PyViCareNotSupportedFeatureError:
            return False


class ZigbeeDevice(Device):

    @handleNotSupported
    def getSerial(self) -> str:
        return str(self.service.getProperty("device.name")["deviceId"])

    @handleNotSupported
    def getZigbeeParentID(self) -> str:
        return str(self.service.getProperty("device.zigbee.parent.id")["properties"]["value"]["value"])

    @handleNotSupported
    def getZigbeeSignalStrength(self) -> int:
        return int(self.service.getProperty("device.zigbee.lqi")["properties"]["strength"]["value"])

    @handleNotSupported
    def getName(self) -> str:
        return str(self.service.getProperty("device.name")["properties"]["name"]["value"])

    @handleAPICommandErrors
    def setName(self, name: str) -> None:
        self.service.setProperty("device.name", "setName", {'name': name})

    @handleNotSupported
    def getIdentification(self) -> bool:
        return bool(self.service.getProperty("device.identification")["properties"]["triggered"]["value"])

    @handleNotSupported
    def getBatteryLevel(self) -> int:
        return int(self.service.getProperty("device.power.battery")["properties"]["level"]["value"])
