from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleAPICommandErrors, handleNotSupported

class FeatureVentilationModePermanent(Device):
    @handleNotSupported
    def getVentilationModePermanentLevels(self) -> list[str]:
        return list[str](self.service.getProperty("ventilation.operating.modes.permanent")["commands"]["setLevel"]["params"]["level"]["constraints"]["enum"])

    @handleAPICommandErrors
    def setVentilationModePermanentLevel(self, level: str):
        return self.service.setProperty("ventilation.operating.modes.permanent", "setLevel", {'level': level})
