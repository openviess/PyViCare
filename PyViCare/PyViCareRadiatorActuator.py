from PyViCare.PyViCareHeatingDevice import HeatingDevice
from PyViCare.PyViCareUtils import handleAPICommandErrors, handleNotSupported


class RadiatorActuator(HeatingDevice):

    @handleNotSupported
    def getTemperature(self):
        return self.service.getProperty("device.sensors.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getTargetTemperature(self):
        return self.service.getProperty("trv.temperature")["properties"]["value"]["value"]

    @handleAPICommandErrors
    def setTargetTemperature(self, temperature):
        return self.service.setProperty("trv.temperature", "setTargetTemperature", {'temperature': int(temperature)})
