import logging

from PyViCare.PyViCareService import ViCareService
from PyViCare.PyViCareUtils import (handleNotSupported)

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

class Device:
    """This is the base class for all devices.
    This class connects to the Viessmann ViCare API.
    The authentication is done through OAuth2.
    Note that currently, a new token is generated for each run.
    """

    def __init__(self, service: ViCareService) -> None:
        self.service = service

    @handleNotSupported
    def getSerial(self):
        return self.service.getProperty("device.serial")["properties"]["value"]["value"]


class DeviceWithComponent:
    """This is the base class for all components"""

    def __init__(self, device: Device, component: str) -> None:
        self.service = device.service
        self.component = component
        self.device = None

    @property
    def id(self) -> str:
        return self.component
