from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleNotSupported


class Gateway(Device):

    @handleNotSupported
    def getSerial(self):
        return self.getProperty("gateway.devices")["gatewayId"]

    @handleNotSupported
    def getWifiSignalStrength(self):
        return self.getProperty("gateway.wifi")["properties"]["strength"]["value"]
