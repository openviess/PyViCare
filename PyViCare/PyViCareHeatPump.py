import re
import json
import os
import logging
from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCare import handleNotSupported

class HeatPump(Device):
    
    @handleNotSupported
    def getCompressorActive(self):
        return self.service.getProperty("heating.compressor")["properties"]["active"]["value"]

    @handleNotSupported
    def getReturnTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]

    @handleNotSupported
    def getCompressorStarts(self):
        return self.service.getProperty("heating.compressor.statistics")["properties"]["starts"]["value"] 

    @handleNotSupported
    def getCompressorHours(self):
        return self.service.getProperty("heating.compressor.statistics")["properties"]["hours"]["value"]

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

    @handleNotSupported
    def getHeatingRodStatusOverall(self):
        return self.service.getProperty("heating.heatingRod.status")["properties"]["overall"]["value"]

    @handleNotSupported
    def getHeatingRodStatusLevel1(self):
        return self.service.getProperty("heating.heatingRod.status")["properties"]["level1"]["value"]
        
    @handleNotSupported
    def getHeatingRodStatusLevel2(self):
        return self.service.getProperty("heating.heatingRod.status")["properties"]["level2"]["value"]
        
    @handleNotSupported
    def getHeatingRodStatusLevel3(self):
        return self.service.getProperty("heating.heatingRod.status")["properties"]["level3"]["value"]
        
    @handleNotSupported
    def getCompressorPower(self):
        """Get compressor power percentage"""
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".sensors.power")["properties"]["value"]["value"]
        
    @handleNotSupported
    def getExpansionValve(self):
        """Get expansion valve percentage"""
        return self.service.getProperty("heating.sensors.valve.expansion")["properties"]["value"]["value"]
        
    @handleNotSupported
    def getSuctionGasPressure(self):
        """Get suction gas pressure in bar"""
        return self.service.getProperty("heating.sensors.pressure.suctionGas")["properties"]["value"]["value"]
        
    @handleNotSupported
    def getHotGasPressure(self):
        """Get hot gas pressure in bar"""
        return self.service.getProperty("heating.sensors.pressure.hotGas")["properties"]["value"]["value"]
        