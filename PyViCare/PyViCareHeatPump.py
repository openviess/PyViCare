import re
import json
import os
import logging
from PyViCare.PyViCareDevice import Device

class HeatPump(Device):
    def getCompressorActive(self):
        try:
            return self.service.getProperty("heating.compressor")["properties"]["active"]["value"]
        except KeyError:
            return "error"
            
    def getReturnTemperature(self):
        try:
            return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getCompressorStarts(self):
        try:
            return self.service.getProperty("heating.compressor.statistics")["properties"]["starts"]["value"]
        except KeyError:
            return "error"   

    def getCompressorHours(self):
        try:
            return self.service.getProperty("heating.compressor.statistics")["properties"]["hours"]["value"]
        except KeyError:
            return "error"

    def getCompressorHoursLoadClass1(self):
        try:
            return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassOne"]["value"]
        except KeyError:
            return "error"

    def getCompressorHoursLoadClass2(self):
        try:
            return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassTwo"]["value"]
        except KeyError:
            return "error"

    def getCompressorHoursLoadClass3(self):
        try:
            return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassThree"]["value"]
        except KeyError:
            return "error"

    def getCompressorHoursLoadClass4(self):
        try:
            return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassFour"]["value"]
        except KeyError:
            return "error"

    def getCompressorHoursLoadClass5(self):
        try:
            return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".statistics")["properties"]["hoursLoadClassFive"]["value"]
        except KeyError:
            return "error"

    def getSupplyTemperaturePrimaryCircuit(self):
        try:
            return self.service.getProperty("heating.primaryCircuit.sensors.temperature.supply")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getReturnTemperaturePrimaryCircuit(self):
        try:
            return self.service.getProperty("heating.primaryCircuit.sensors.temperature.return")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getHeatingRodStatusOverall(self):
        try:
            return self.service.getProperty("heating.heatingRod.status")["properties"]["overall"]["value"]
        except KeyError:
            return "error"

    def getHeatingRodStatusLevel1(self):
        try:
            return self.service.getProperty("heating.heatingRod.status")["properties"]["level1"]["value"]
        except KeyError:
            return "error"

    def getHeatingRodStatusLevel2(self):
        try:
            return self.service.getProperty("heating.heatingRod.status")["properties"]["level2"]["value"]
        except KeyError:
            return "error"

    def getHeatingRodStatusLevel3(self):
        try:
            return self.service.getProperty("heating.heatingRod.status")["properties"]["level3"]["value"]
        except KeyError:
            return "error"

    def getCompressorPower(self):
        """Get compressor power percentage"""
        try:
            return self.service.getProperty("heating.compressors." + str(self.service.circuit) + ".sensors.power")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getExpansionValve(self):
        """Get expansion valve percentage"""
        try:
            return self.service.getProperty("heating.sensors.valve.expansion")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getSuctionGasPressure(self):
        """Get suction gas pressure in bar"""
        try:
            return self.service.getProperty("heating.sensors.pressure.suctionGas")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getHotGasPressure(self):
        """Get hot gas pressure in bar"""
        try:
            return self.service.getProperty("heating.sensors.pressure.hotGas")["properties"]["value"]["value"]
        except KeyError:
            return "error"
