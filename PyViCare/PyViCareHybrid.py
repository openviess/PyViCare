from PyViCare.PyViCareGazBoiler import GazBoiler, GazBoilerWithCircuit
from PyViCare.PyViCareHeatPump import HeatPump, HeatPumpWithCircuit


class Hybrid(GazBoiler, HeatPump):
    def getCircuit(self, circuit):
        return HybridWithCircuit(self, circuit)

class HybridWithCircuit(GazBoilerWithCircuit, HeatPumpWithCircuit):
    pass