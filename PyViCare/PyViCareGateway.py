from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleNotSupported


class Gateway(Device):

    @handleNotSupported
    def getWifiSignalStrength(self):
        return self.service.getProperty("gateway.wifi")["properties"]["strength"]["value"]
