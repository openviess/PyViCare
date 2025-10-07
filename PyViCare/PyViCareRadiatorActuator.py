from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleAPICommandErrors, handleNotSupported


class RadiatorActuator(Device):

    @handleNotSupported
    def getSerial(self):
        return self.service.getProperty("device.name")["deviceId"]

    @handleNotSupported
    def getBatteryLevel(self) -> int:
        return int(self.service.getProperty("device.power.battery")["properties"]["level"]["value"])

    @handleNotSupported
    def getTemperature(self):
        return self.service.getProperty("device.sensors.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getValvePosition(self) -> int:
        return int(self.service.getProperty("trv.valve.position")["properties"]["position"]["value"])

    @handleNotSupported
    def getChildLock(self) -> str:
        return str(self.service.getProperty("trv.childLock")["properties"]["status"]["value"])

    @handleNotSupported
    def getMountingMode(self) -> boolean:
        return boolean(self.service.getProperty("trv.mountingMode")["properties"]["active"]["value"])

    @handleNotSupported
    def getZigbeeLinkQuality(self) -> int:
        return int(self.service.getProperty("device.zigbee.lqi")["properties"]["strength"]["value"])

    @handleNotSupported
    def getTargetTemperature(self):
        return self.service.getProperty("trv.temperature")["properties"]["value"]["value"]

    @handleAPICommandErrors
    def setTargetTemperature(self, temperature):
        return self.service.setProperty("trv.temperature", "setTargetTemperature", {'temperature': float(temperature)})
