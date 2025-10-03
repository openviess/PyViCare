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
        # Zigbee TRV reports temperature under trv.temperature, not device.sensors.temperature
        return self.service.getProperty("trv.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getValvePosition(self):
        return self.service.getProperty("trv.valve.position")["properties"]["position"]["value"]

    @handleNotSupported
    def getChildLockStatus(self):
        return self.service.getProperty("trv.childLock")["properties"]["status"]["value"]

    @handleNotSupported
    def getMountingModeActive(self):
        return self.service.getProperty("trv.mountingMode")["properties"]["active"]["value"]

    @handleNotSupported
    def getLinkQuality(self):
        return self.service.getProperty("device.zigbee.lqi")["properties"]["strength"]["value"]

    @handleNotSupported
    def getTargetTemperature(self):
        # note: this is the *setpoint* value, read-only unless API exposes write
        return self.service.getProperty("trv.temperature")["properties"]["value"]["value"]

