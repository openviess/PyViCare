from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCare import handleNotSupported

class HeatPump(Device):
    
    @handleNotSupported
    def getCompressorActive(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit))["properties"]["active"]["value"]

    @handleNotSupported
    def getReturnTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]

    @handleNotSupported
    def getCompressorStarts(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["starts"]["value"] 

    @handleNotSupported
    def getCompressorHours(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hours"]["value"]

    @handleNotSupported
    def getCompressorHoursLoadClass1(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassOne"]["value"]

    @handleNotSupported
    def getCompressorHoursLoadClass2(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassTwo"]["value"]

    @handleNotSupported
    def getCompressorHoursLoadClass3(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassThree"]["value"]

    @handleNotSupported
    def getCompressorHoursLoadClass4(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassFour"]["value"]

    @handleNotSupported
    def getCompressorHoursLoadClass5(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassFive"]["value"]

    @handleNotSupported
    def getSupplyTemperaturePrimaryCircuit(self):
        return self.service.getProperty("heating.primaryCircuit.sensors.temperature.supply")["properties"]["value"]["value"]

    @handleNotSupported
    def getReturnTemperaturePrimaryCircuit(self):
        return self.service.getProperty("heating.primaryCircuit.sensors.temperature.return")["properties"]["value"]["value"]