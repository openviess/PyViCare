from PyViCare.PyViCareDevice import ZigbeeDevice, Device
from PyViCare.PyViCareUtils import handleAPICommandErrors, handleNotSupported


class FloorHeating(ZigbeeDevice):

    @handleNotSupported
    def getSupplyTemperature(self) -> float:
        return float(self.getProperty("fht.sensors.temperature.supply")["properties"]["value"]["value"])

    @handleNotSupported
    def getActiveMode(self) -> str:
        return str(self.getProperty("fht.operating.modes.active")["properties"]["value"]["value"])


class FloorHeatingChannel(Device):

    @handleNotSupported
    def getSerial(self) -> str:
        return str(self.getProperty("device.name")["deviceId"])

    @handleNotSupported
    def getName(self) -> str:
        return str(self.getProperty("device.name")["properties"]["name"]["value"])

    @handleAPICommandErrors
    def setName(self, name: str) -> None:
        self.setProperty("device.name", "setName", {'name': name})

    @handleNotSupported
    def getValveState(self) -> str:
        return str(self.getProperty("fht.valve.state")["properties"]["status"]["value"])

    @handleNotSupported
    def isValveOpen(self) -> bool:
        return bool(self.getValveState() != "closed")
