import re
import json
import os
import logging
from .PyViCareService import ViCareService

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

# TODO Holiday program can still be used (parameters are there) heating.circuits." + str(self.service.circuit) + ".operating.programs.holiday
# TODO heating.dhw.schedule/setSchedule

""""Viessmann ViCare API Python tools"""

class ViCareHeatPumpSession:
    """This class connects to the Viesmann ViCare API.
    The authentication is done through OAuth2.
    Note that currently, a new token is generate for each run.
    """


    def __init__(self, username, password,token_file=None,circuit=0):
        """Init function. Create the necessary oAuth2 sessions
        Parameters
        ----------
        username : str
            e-mail address
        password : str
            password

        Returns
        -------
        """

        self.service = ViCareService(username, password, token_file, circuit)

    """ Set the active mode
    Parameters
    ----------
    mode : str
        Valid mode can be obtained using getModes()

    Returns
    -------
    result: json
        json representation of the answer
    """
    def setMode(self,mode):
        r=self.service.setProperty("heating.circuits." + str(self.service.circuit) + ".operating.modes.active","setMode","{\"mode\":\""+mode+"\"}")
        return r

    # Works for normal, reduced, comfort
    # active has no action
    # exetenral , standby no action
    # holiday, sheculde and unscheduled
    # activate, decativate comfort,eco
    """ Set the target temperature for the target program
    Parameters
    ----------
    program : str
        Can be normal, reduced or comfort
    temperature: int
        target temperature

    Returns
    -------
    result: json
        json representation of the answer
    """
    def setProgramTemperature(self,program: str,temperature :int):
        return self.service.setProperty("heating.circuits." + str(self.service.circuit) + ".operating.programs."+program,"setTemperature","{\"targetTemperature\":"+str(temperature)+"}")

    def setReducedTemperature(self,temperature):
        return self.setProgramTemperature("reduced",temperature)

    def setComfortTemperature(self,temperature):
        return self.setProgramTemperature("comfort",temperature)

    def setNormalTemperature(self,temperature):
        return self.setProgramTemperature("normal",temperature)

    """ Activate a program
        NOTE
        DEVICE_COMMUNICATION_ERROR can just mean that the program is already on
    Parameters
    ----------
    program : str
        Appears to work only for comfort

    Returns
    -------
    result: json
        json representation of the answer
    """
    # optional temperature parameter could be passed (but not done)
    def activateProgram(self,program):
        return self.service.setProperty("heating.circuits." + str(self.service.circuit) + ".operating.programs."+program,"activate","{}")

    def activateComfort(self):
        return self.activateProgram("comfort")
    """ Deactivate a program
    Parameters
    ----------
    program : str
        Appears to work only for comfort and eco (coming from normal, can be reached only by deactivating another state)

    Returns
    -------
    result: json
        json representation of the answer
    """
    def deactivateProgram(self,program):
        return self.service.setProperty("heating.circuits." + str(self.service.circuit) + ".operating.programs."+program,"deactivate","{}")
    def deactivateComfort(self):
        return self.deactivateProgram("comfort")

    def getOutsideTemperature(self):
        try:
            return self.service.getProperty("heating.sensors.temperature.outside")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getSupplyTemperature(self):
        try:
            return self.service.getProperty("heating.circuits." + str(self.service.circuit) + ".sensors.temperature.supply")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getModes(self):
        try:
            return self.service.getProperty("heating.circuits." + str(self.service.circuit) + ".operating.modes.active")["actions"][0]["fields"][0]["enum"]
        except KeyError:
            return "error"

    def getActiveMode(self):
        try:
            return self.service.getProperty("heating.circuits." + str(self.service.circuit) + ".operating.modes.active")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getHeatingCurveShift(self):
        try:
            return self.service.getProperty("heating.circuits." + str(self.service.circuit) + ".heating.curve")["properties"]["shift"]["value"]
        except KeyError:
            return "error"

    def getHeatingCurveSlope(self):
        try:
            return self.service.getProperty("heating.circuits." + str(self.service.circuit) + ".heating.curve")["properties"]["slope"]["value"]
        except KeyError:
            return "error"

    def getActiveProgram(self):
        try:
            return self.service.getProperty("heating.circuits." + str(self.service.circuit) + ".operating.programs.active")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getPrograms(self):
        try:
            return self.service.getProperty("heating.circuits." + str(self.service.circuit) + ".operating.programs")["entities"][9]["properties"]["components"]
        except KeyError:
            return "error"

    def getDesiredTemperatureForProgram(self , program):
        try:
            return self.service.getProperty("heating.circuits." + str(self.service.circuit) + ".operating.programs."+program)["properties"]["temperature"]["value"]
        except KeyError:
            return "error"

    def getCurrentDesiredTemperature(self):
        try:
            activeProgram = self.getActiveProgram()
            if activeProgram == 'standby':
                return self.getDesiredTemperatureForProgram('normal')
            else:
                return self.getDesiredTemperatureForProgram(activeProgram)
        except KeyError:
            return "error"

    def getDomesticHotWaterConfiguredTemperature(self):
        try:
            return self.service.getProperty("heating.dhw.temperature")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getDomesticHotWaterStorageTemperature(self):
        try:
            return self.service.getProperty("heating.dhw.sensors.temperature.hotWaterStorage")["properties"]["value"]["value"]
        except KeyError:
            return "error"

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

    def getErrorHistory(self):
        try:
            return self.service.getProperty("heating.errors.history")["properties"]["entries"]["value"]
        except KeyError:
            return "error"

    def getActiveError(self):
        try:
            return self.service.getProperty("heating.errors.active")["properties"]["entries"]["value"]
        except KeyError:
            return "error"

    def getReturnTemperature(self):
        try:
            return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]
        except KeyError:
            return "error"

    def getCirculationPumpActive(self):
        try:
            status =  self.service.getProperty("heating.circuits." + str(self.service.circuit) + ".circulation.pump")["properties"]["status"]["value"]
            return status == 'on'
        except KeyError:
            return "error"

    def getCompressorActive(self):
        try:
            return self.service.getProperty("heating.compressor")["properties"]["active"]["value"]
        except KeyError:
            return "error"
