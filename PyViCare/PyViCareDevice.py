from PyViCare.PyViCareService import ViCareService
from PyViCare.PyViCareUtils import handleNotSupported


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
