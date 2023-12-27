from contextlib import suppress

from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import (PyViCareNotSupportedFeatureError, handleAPICommandErrors, handleNotSupported)


class VentilationDevice(Device):
    """This is the base class for all ventilation devices.
    This class connects to the Viessmann ViCare API.
    The authentication is done through OAuth2.
    Note that currently, a new token is generated for each run.
    """

    @handleNotSupported
    def getAvailableModes(self):
        return self.service.getProperty("ventilation.operating.modes.active")["commands"]["setMode"]["params"]["mode"]["constraints"]["enum"]

    @handleNotSupported
    def getActiveMode(self):
        return self.service.getProperty("ventilation.operating.modes.active")["properties"]["value"]["value"]

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
    def setActiveMode(self, mode):
        return self.service.setProperty("ventilation.operating.modes.active", "setMode", {'mode': mode})

    @handleNotSupported
    def getAvailablePrograms(self):
        available_programs = []
        for program in ['basic', 'intensive', 'reduced', 'standard', 'standby', 'comfort', 'eco', 'forcedLevelFour',
                        'holiday', 'holidayAtHome', 'levelFour', 'levelOne', 'levelThree', 'levelTwo', 'permanent', 'silent']:
            with suppress(PyViCareNotSupportedFeatureError):
                if self.service.getProperty(f"ventilation.operating.programs.{program}") is not None:
                    available_programs.append(program)
        return available_programs

    @handleNotSupported
    def getActiveProgram(self):
        return self.service.getProperty("ventilation.operating.programs.active")["properties"]["value"]["value"]

    """ Activate a program
        NOTE
        DEVICE_COMMUNICATION_ERROR can just mean that the program is already on
    Parameters
    ----------
    program : str

    Returns
    -------
    result: json
        json representation of the answer
    """
    def activateProgram(self, program):
        return self.service.setProperty(f"ventilation.operating.programs.{program}", "activate", {})

    """ Deactivate a program
    Parameters
    ----------
    program : str

    Returns
    -------
    result: json
        json representation of the answer
    """
    def deactivateProgram(self, program):
        return self.service.setProperty(f"ventilation.operating.programs.{program}", "deactivate", {})

    @handleAPICommandErrors
    def setPermanentLevel(self, level: str):
        return self.service.setProperty("ventilation.operating.modes.permanent", "setLevel", {'level': level})

    @handleNotSupported
    def getSchedule(self):
        properties = self.service.getProperty("ventilation.schedule")["properties"]
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
