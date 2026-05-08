from PyViCare.PyViCareDevice import ZigbeeBatteryDevice
from PyViCare.PyViCareUtils import handleNotSupported


class RoomSensor(ZigbeeBatteryDevice):

    @handleNotSupported
    def getSerial(self) -> str:
        return str(self.getProperty("device.sensors.temperature")["deviceId"])

    @handleNotSupported
    def getTemperature(self) -> float:
        return float(self.getProperty("device.sensors.temperature")["properties"]["value"]["value"])

    @handleNotSupported
    def getHumidity(self) -> float:
        return float(self.getProperty("device.sensors.humidity")["properties"]["value"]["value"])
