from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareVentilationDevice import VentilationDevice


class Hybrid(GazBoiler, HeatPump):
    pass

class HeatPumpWithVentilation(HeatPump, VentilationDevice):
    pass
