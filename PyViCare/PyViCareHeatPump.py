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
