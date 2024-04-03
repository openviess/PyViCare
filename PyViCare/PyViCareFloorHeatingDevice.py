from PyViCare.PyViCareHeatingDevice import HeatingDevice
from PyViCare.PyViCareUtils import handleNotSupported


class RadiatorActuator(HeatingDevice):

    @handleNotSupported
    def getSupplyTemperature(self):
        return self.service.getProperty("fht.sensors.temperature.supply")["properties"]["value"]["value"]

    @handleNotSupported
    def getActiveMode(self):
        return self.service.getProperty("fht.operating.modes.active")["properties"]["value"]["value"]
