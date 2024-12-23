from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareUtils import handleNotSupported

class FeatureVentilationState(Device):
    @handleNotSupported
    def getVentilationDemand(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["demand"]["value"])

    @handleNotSupported
    def getVentilationLevel(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["level"]["value"])

    @handleNotSupported
    def getVentilationReason(self) -> str:
        return str(self.service.getProperty("ventilation.operating.state")["properties"]["reason"]["value"])
