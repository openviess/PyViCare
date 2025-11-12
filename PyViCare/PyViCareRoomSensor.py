from PyViCare.PyViCareDevice import ZigbeeBatteryDevice
from PyViCare.PyViCareUtils import handleNotSupported


class RoomSensor(ZigbeeBatteryDevice):

    @handleNotSupported
    def getSerial(self):
        return self.getProperty("device.sensors.temperature")["deviceId"]

    @handleNotSupported
    def getTemperature(self):
        return self.getProperty("device.sensors.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getHumidity(self):
        return self.getProperty("device.sensors.humidity")["properties"]["value"]["value"]
