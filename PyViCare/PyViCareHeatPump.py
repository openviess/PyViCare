import re
import json
import os
import logging
from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCare import handleKeyError

class HeatPump(Device):
    
    @handleKeyError
    def getCompressorActive(self):
        return self.service.getProperty("heating.compressor")["properties"]["active"]["value"]

    @handleKeyError
    def getReturnTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]

    @handleKeyError
    def getCompressorStarts(self):
        return self.service.getProperty("heating.compressor.statistics")["properties"]["starts"]["value"] 

    @handleKeyError
    def getCompressorHours(self):
        return self.service.getProperty("heating.compressor.statistics")["properties"]["hours"]["value"]

    @handleKeyError
    def getCompressorHoursLoadClass1(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassOne"]["value"]

    @handleKeyError
    def getCompressorHoursLoadClass2(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassTwo"]["value"]

    @handleKeyError
    def getCompressorHoursLoadClass3(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassThree"]["value"]

    @handleKeyError
    def getCompressorHoursLoadClass4(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassFour"]["value"]

    @handleKeyError
    def getCompressorHoursLoadClass5(self):
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassFive"]["value"]

    @handleKeyError
    def getSupplyTemperaturePrimaryCircuit(self):
        return self.service.getProperty("heating.primaryCircuit.sensors.temperature.supply")["properties"]["value"]["value"]

    @handleKeyError
    def getReturnTemperaturePrimaryCircuit(self):
        return self.service.getProperty("heating.primaryCircuit.sensors.temperature.return")["properties"]["value"]["value"]

    @handleKeyError
    def getHeatingRodStatusOverall(self):
        return self.service.getProperty("heating.heatingRod.status")["properties"]["overall"]["value"]

    @handleKeyError
    def getHeatingRodStatusLevel1(self):
        return self.service.getProperty("heating.heatingRod.status")["properties"]["level1"]["value"]
        
    @handleKeyError
    def getHeatingRodStatusLevel2(self):
        return self.service.getProperty("heating.heatingRod.status")["properties"]["level2"]["value"]
        
    @handleKeyError
    def getHeatingRodStatusLevel3(self):
        return self.service.getProperty("heating.heatingRod.status")["properties"]["level3"]["value"]
        
    @handleKeyError
    def getCompressorPower(self):
        """Get compressor power percentage"""
        return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".sensors.power")["properties"]["value"]["value"]
        
    @handleKeyError
    def getExpansionValve(self):
        """Get expansion valve percentage"""
        return self.service.getProperty("heating.sensors.valve.expansion")["properties"]["value"]["value"]
        
    @handleKeyError
    def getSuctionGasPressure(self):
        """Get suction gas pressure in bar"""
        return self.service.getProperty("heating.sensors.pressure.suctionGas")["properties"]["value"]["value"]
        
    @handleKeyError
    def getHotGasPressure(self):
        """Get hot gas pressure in bar"""
        return self.service.getProperty("heating.sensors.pressure.hotGas")["properties"]["value"]["value"]
        