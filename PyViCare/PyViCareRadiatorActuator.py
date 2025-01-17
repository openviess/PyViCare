from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleAPICommandErrors, handleNotSupported


class RadiatorActuator(Device):

    @handleNotSupported
    def getSerial(self):
        return self.service.getProperty("device.name")["deviceId"]

    @handleNotSupported
    def getTemperature(self):
        return self.service.getProperty("device.sensors.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getTargetTemperature(self):
        return self.service.getProperty("trv.temperature")["properties"]["value"]["value"]

    @handleAPICommandErrors
    def setTargetTemperature(self, temperature):
        return self.service.setProperty("trv.temperature", "setTargetTemperature", {'temperature': float(temperature)})
