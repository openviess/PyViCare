from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleNotSupported

class FeatureVentilationModes(Device):
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
