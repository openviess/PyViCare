from contextlib import suppress

from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError, handleAPICommandErrors, handleNotSupported

class FeatureVentilation(Device):
    @handleNotSupported
    def getVentilationDemand(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["demand"]["value"])

    @handleNotSupported
    def getVentilationLevel(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["level"]["value"])

    @handleNotSupported
    def getVentilationReason(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["reason"]["value"])

    @handleNotSupported
    def getVentilationModes(self) -> list[str]:
        return list[str](self.service.getProperty("ventilation.operating.modes.active")["commands"]["setMode"]["params"]["mode"]["constraints"]["enum"])

    @handleNotSupported
    def getVentilationMode(self, mode: str) -> bool:
        return bool(self.service.getProperty(f"ventilation.operating.modes.{mode}")["properties"]["active"]["value"])

    @handleNotSupported
    def getActiveVentilationMode(self) -> str:
        return str(self.service.getProperty("ventilation.operating.modes.active")["properties"]["value"]["value"])

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

    @handleNotSupported
    def getVentilationModePermanentLevels(self) -> list[str]:
        return list[str](self.service.getProperty("ventilation.operating.modes.permanent")["commands"]["setLevel"]["params"]["level"]["constraints"]["enum"])

    @handleAPICommandErrors
    def setVentilationModePermanentLevel(self, level: str):
        return self.service.setProperty("ventilation.operating.modes.permanent", "setLevel", {'level': level})

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
