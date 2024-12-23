from contextlib import suppress

from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import (PyViCareNotSupportedFeatureError, handleNotSupported)

class FeatureVentilationQuickmodes(Device):
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
