from PyViCare2.PyViCareDevice import Device
from PyViCare2.PyViCareUtils import handleNotSupported


class RoomSensor(Device):

    @handleNotSupported
    def getSerial(self):
        return self.service.getProperty("device.sensors.temperature")["deviceId"]

    @handleNotSupported
    def getBatteryLevel(self) -> int:
        return int(self.service.getProperty("device.power.battery")["properties"]["level"]["value"])

    @handleNotSupported
    def getTemperature(self):
        return self.service.getProperty("device.sensors.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getHumidity(self):
        return self.service.getProperty("device.sensors.humidity")["properties"]["value"]["value"]
