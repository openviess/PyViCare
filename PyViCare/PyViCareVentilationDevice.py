
from contextlib import suppress

from PyViCare.Features.FeatureVentilationQuickmodes import FeatureVentilationQuickmodes
from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import (PyViCareNotSupportedFeatureError, handleAPICommandErrors, handleNotSupported)


class VentilationDevice(FeatureVentilationQuickmodes, Device):
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

    def setActiveMode(self, mode):
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
        return self.service.setProperty("ventilation.operating.modes.active", "setMode", {'mode': mode})

    @handleNotSupported
    def getAvailablePrograms(self):
        available_programs = []
        for program in ['basic', 'intensive', 'reduced', 'standard', 'standby', 'holidayAtHome', 'permanent']:
            with suppress(PyViCareNotSupportedFeatureError):
                if self.service.getProperty(f"ventilation.operating.programs.{program}") is not None:
                    available_programs.append(program)
        return available_programs

    @handleNotSupported
    def getActiveProgram(self):
        return self.service.getProperty("ventilation.operating.programs.active")["properties"]["value"]["value"]

    def activateProgram(self, program):
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
        return self.service.setProperty(f"ventilation.operating.programs.{program}", "activate", {})

    def deactivateProgram(self, program):
        """ Deactivate a program
        Parameters
        ----------
        program : str

        Returns
        -------
        result: json
            json representation of the answer
        """
        return self.service.setProperty(f"ventilation.operating.programs.{program}", "deactivate", {})

    @handleNotSupported
    def getPermanentLevels(self) -> list[str]:
        return list[str](self.service.getProperty("ventilation.operating.modes.permanent")["commands"]["setLevel"]["params"]["level"]["constraints"]["enum"])

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

    @handleNotSupported
    def getVentilationDemand(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["demand"]["value"])

    @handleNotSupported
    def getVentilationLevel(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["level"]["value"])

    @handleNotSupported
    def getVentilationReason(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["reason"]["value"])

