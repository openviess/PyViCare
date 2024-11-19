from typing import Any

from PyViCare.PyViCareService import ViCareService
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError, handleNotSupported


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
