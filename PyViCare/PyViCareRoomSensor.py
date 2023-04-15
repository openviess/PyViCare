from PyViCare.PyViCareHeatingDevice import HeatingDevice
from PyViCare.PyViCareUtils import handleNotSupported


class RoomSensor(HeatingDevice):

    @handleNotSupported
    def getTemperature(self):
        return self.service.getProperty("device.sensors.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getHumidity(self):
        return self.service.getProperty("device.sensors.humidity")["properties"]["value"]["value"]
