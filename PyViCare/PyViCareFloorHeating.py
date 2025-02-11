from PyViCare.PyViCareHeatingDevice import HeatingDevice
from PyViCare.PyViCareUtils import handleNotSupported


class FloorHeating(HeatingDevice):

    @handleNotSupported
    def getSerial(self):
        return self.service.getProperty("device.name")["deviceId"]

    @handleNotSupported
    def getSupplyTemperature(self):
        return self.service.getProperty("fht.sensors.temperature.supply")["properties"]["value"]["value"]

    @handleNotSupported
    def getModes(self):
        return self.service.getProperty("fht.operating.modes.active")["commands"]["setMode"]["params"]["mode"]["constraints"]["enum"]

    @handleNotSupported
    def getActiveMode(self):
        return self.service.getProperty("fht.operating.modes.active")["properties"]["value"]["value"]

    def setMode(self, mode):
        """ Set the active mode
        Parameters
        ----------
        mode : str
            Valid mode can be obtained using getModes()

        Returns
        -------
        result: json
            json representation of the answer
        """
        return self.service.setProperty("fht.operating.modes.active", "setMode", {'mode': mode})
