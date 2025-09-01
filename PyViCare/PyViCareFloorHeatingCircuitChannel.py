from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleNotSupported


class FloorHeatingCircuitChannel(Device):

    @handleNotSupported
    def getSerial(self):
        return self.service.getProperty("device.name")["deviceId"]

    @handleNotSupported
    def getName(self):
        return self.service.getProperty("device.name")["properties"]["name"]["value"]
