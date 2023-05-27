from typing import Any, List

from PyViCare.PyViCareHeatingDevice import (HeatingDevice,
                                            get_available_burners)
from PyViCare.PyViCareUtils import handleNotSupported

class ElectricalEnergySystem(HeatingDevice):

    @property
    @handleNotSupported
    def getTransferPowerExchange(self):
        return self.service.getProperty("pcc.transfer.power.exchange")["properties"]["value"]["value"]

    
