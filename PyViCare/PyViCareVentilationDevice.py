from contextlib import suppress
from deprecated import deprecated

from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import (PyViCareNotSupportedFeatureError, handleAPICommandErrors, handleNotSupported)


class VentilationDevice(Device):
    """This is the base class for all ventilation devices.
    This class connects to the Viessmann ViCare API.
    The authentication is done through OAuth2.
    Note that currently, a new token is generated for each run.
    """

    @handleNotSupported
    def getVentilationDemand(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["demand"]["value"])

    @handleNotSupported
    def getVentilationReason(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["reason"]["value"])

    @handleNotSupported
    def getVentilationModes(self) -> list[str]:
        return list[str](self.service.getProperty("ventilation.operating.modes.active")["commands"]["setMode"]["params"]["mode"]["constraints"]["enum"])

    @handleNotSupported
    @deprecated(reason="renamed, use getVentilationModes", version="2.40.0")
    def getAvailableModes(self):
        return self.getVentilationModes()

    @handleNotSupported
    def getVentilationMode(self, mode: str) -> bool:
        return bool(self.service.getProperty(f"ventilation.operating.modes.{mode}")["properties"]["active"]["value"])

    @handleNotSupported
    def getActiveVentilationMode(self) -> str:
        return str(self.service.getProperty("ventilation.operating.modes.active")["properties"]["value"]["value"])

    @handleNotSupported
    def getVentilationLevels(self) -> list[str]:
        return list[str](self.service.getProperty("ventilation.operating.modes.permanent")["commands"]["setLevel"]["params"]["level"]["constraints"]["enum"])

    @handleNotSupported
    @deprecated(reason="renamed, use getVentilationLevels", version="2.40.0")
    def getPermanentLevels(self) -> list[str]:
        return list[str](self.getVentilationLevels())

    @handleNotSupported
    def getVentilationLevel(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["level"]["value"])

    @handleAPICommandErrors
    def setVentilationLevel(self, level: str):
        return self.service.setProperty("ventilation.operating.modes.permanent", "setLevel", {'level': level})

    @handleAPICommandErrors
    @deprecated(reason="renamed, use setVentilationLevel", version="2.40.0")
    def setPermanentLevel(self, level: str):
        return self.setVentilationLevel(level)

    @handleNotSupported
    @deprecated(reason="renamed, use getActiveVentilationMode", version="2.40.0")
    def getActiveMode(self):
        return self.getActiveVentilationMode()

    def activateVentilationMode(self, mode: str):
        """ Set the active ventilation mode
        Parameters
        ----------
        mode : str
            Valid mode can be obtained using getVentilationModes()

        Returns
        -------
        result: json
            json representation of the answer
        """
        return self.service.setProperty("ventilation.operating.modes.active", "setMode", {'mode': mode})

    @deprecated(reason="renamed, use activateVentilationMode", version="2.40.0")
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
        return self.activateVentilationMode(mode)

    @handleNotSupported
    def getVentilationQuickmodes(self) -> list[str]:
        available_quickmodes = []
        for quickmode in ['comfort', 'eco', 'forcedLevelFour', 'holiday', 'standby', 'silent']:
            with suppress(PyViCareNotSupportedFeatureError):
                if self.service.getProperty(f"ventilation.quickmodes.{quickmode}") is not None:
                    available_quickmodes.append(quickmode)
        return available_quickmodes

    @handleNotSupported
    def getVentilationQuickmode(self, quickmode: str) -> bool:
        return bool(self.service.getProperty(f"ventilation.quickmodes.{quickmode}")["properties"]["active"]["value"])

    @handleNotSupported
    def activateVentilationQuickmode(self, quickmode: str) -> None:
        self.service.setProperty(f"ventilation.quickmodes.{quickmode}", "activate", {})

    @handleNotSupported
    def deactivateVentilationQuickmode(self, quickmode: str) -> None:
        self.service.setProperty(f"ventilation.quickmodes.{quickmode}", "deactivate", {})

    @handleNotSupported
    def getVentilationPrograms(self):
        available_programs = []
        for program in ['basic', 'intensive', 'reduced', 'standard', 'standby', 'holidayAtHome', 'permanent']:
            with suppress(PyViCareNotSupportedFeatureError):
                if self.service.getProperty(f"ventilation.operating.programs.{program}") is not None:
                    available_programs.append(program)
        return available_programs

    @handleNotSupported
    @deprecated(reason="renamed, use getVentilationPrograms", version="2.40.0")
    def getAvailablePrograms(self):
        return self.getVentilationPrograms()

    @handleNotSupported
    def getActiveVentilationProgram(self):
        return self.service.getProperty("ventilation.operating.programs.active")["properties"]["value"]["value"]

    @handleNotSupported
    @deprecated(reason="renamed, use getActiveVentilationProgram", version="2.40.0")
    def getActiveProgram(self):
        return self.getActiveVentilationProgram()

    def activateVentilationProgram(self, program):
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

    @deprecated(reason="renamed, use activateVentilationProgram", version="2.40.0")
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
        return self.activateVentilationProgram(program)

    def deactivateVentilationProgram(self, program):
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

    @deprecated(reason="renamed, use deactivateVentilationProgram", version="2.40.0")
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
        return self.deactivateVentilationProgram(program)

    @handleNotSupported
    def getVentilationSchedule(self):
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
    @deprecated(reason="renamed, use getVentilationSchedule", version="2.40.0")
    def getSchedule(self):
        return self.getVentilationSchedule()
