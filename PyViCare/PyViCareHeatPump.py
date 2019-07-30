import re
import json
import os
import logging
from PyViCare.PyViCareDevice import Device

class HeatPump(Device):

    def getHeatingSchedule(self):
        try:
            properties = self.service.getProperty("heating.circuits." + str(self.service.circuit) + ".heating.schedule")["properties"]
            return {
                "active": properties["active"]["value"],
                "mon": properties["entries"]["value"]["mon"],
                "tue": properties["entries"]["value"]["tue"],
                "wed": properties["entries"]["value"]["wed"],
                "thu": properties["entries"]["value"]["thu"],
                "fri": properties["entries"]["value"]["fri"],
                "sat": properties["entries"]["value"]["sat"],
                "sun": properties["entries"]["value"]["sun"]
            }
        except KeyError:
            return "error"

    def getDomesticHotWaterSchedule(self):
        try:
            properties = self.service.getProperty("heating.dhw.schedule")["properties"]
            return {
                "active": properties["active"]["value"],
                "mon": properties["entries"]["value"]["mon"],
                "tue": properties["entries"]["value"]["tue"],
                "wed": properties["entries"]["value"]["wed"],
                "thu": properties["entries"]["value"]["thu"],
                "fri": properties["entries"]["value"]["fri"],
                "sat": properties["entries"]["value"]["sat"],
                "sun": properties["entries"]["value"]["sun"]
            }
        except KeyError:
            return "error"


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