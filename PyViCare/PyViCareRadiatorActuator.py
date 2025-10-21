from PyViCare.PyViCareDevice import ZigbeeBatteryDevice
from PyViCare.PyViCareUtils import handleAPICommandErrors, handleNotSupported


class RadiatorActuator(ZigbeeBatteryDevice):

    @handleNotSupported
    def getTemperature(self):
        return self.getProperty("device.sensors.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getValvePosition(self) -> int:
        return int(self.getProperty("trv.valve.position")["properties"]["position"]["value"])

    @handleNotSupported
    def isValveOpen(self) -> bool:
        return bool(self.getValvePosition() > 0)

    @handleNotSupported
    def getChildLock(self) -> str:
        return str(self.getProperty("trv.childLock")["properties"]["status"]["value"])

    @handleNotSupported
    def getMountingMode(self) -> bool:
        return bool(self.getProperty("trv.mountingMode")["properties"]["active"]["value"])

    @handleNotSupported
    def getTargetTemperature(self):
        return self.getProperty("trv.temperature")["properties"]["value"]["value"]

    @handleAPICommandErrors
    def setTargetTemperature(self, temperature):
        return self.setProperty("trv.temperature", "setTargetTemperature", {'temperature': float(temperature)})
