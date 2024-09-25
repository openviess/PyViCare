from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleNotSupported


class RoomSensor(Device):

    @handleNotSupported
    def getSerial(self):
        return self.service.getProperty("device.sensors.temperature")["deviceId"]

    @handleNotSupported
    def getTemperature(self):
        return self.service.getProperty("device.sensors.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getHumidity(self):
        return self.service.getProperty("device.sensors.humidity")["properties"]["value"]["value"]
