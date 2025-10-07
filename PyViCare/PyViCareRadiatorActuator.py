from PyViCare.PyViCareDevice import ZigbeeDevice
from PyViCare.PyViCareUtils import handleAPICommandErrors, handleNotSupported


class RadiatorActuator(ZigbeeDevice):

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
    def getMountingMode(self) -> bool:
        return bool(self.service.getProperty("trv.mountingMode")["properties"]["active"]["value"])

    @handleNotSupported
    def getTargetTemperature(self):
        return self.service.getProperty("trv.temperature")["properties"]["value"]["value"]

    @handleAPICommandErrors
    def setTargetTemperature(self, temperature):
        return self.service.setProperty("trv.temperature", "setTargetTemperature", {'temperature': float(temperature)})
