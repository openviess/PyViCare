from PyViCare2.PyViCareDevice import Device
from PyViCare2.PyViCareUtils import handleNotSupported


class Gateway(Device):

    @handleNotSupported
    def getSerial(self):
        return self.service.getProperty("gateway.devices")["gatewayId"]

    @handleNotSupported
    def getWifiSignalStrength(self):
        return self.service.getProperty("gateway.wifi")["properties"]["strength"]["value"]
