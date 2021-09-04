from typing import Any, List

from PyViCare.PyViCareDevice import Device, DeviceWithComponent
from PyViCare.PyViCareUtils import handleNotSupported


class HeatPump(Device):

    @property
    def compressors(self) -> List[Any]:
        return list([self.getCompressor(x) for x in self.getAvailableCompressors()])

    def getCompressor(self, compressor):
        return Compressor(self, compressor)

    @handleNotSupported
    def getAvailableCompressors(self):
        return self.service.getProperty("heating.compressors")["components"]

    @handleNotSupported
    def getReturnTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]

    @handleNotSupported
    def getSupplyTemperaturePrimaryCircuit(self):
        return self.service.getProperty("heating.primaryCircuit.sensors.temperature.supply")["properties"]["value"]["value"]

    @handleNotSupported
    def getReturnTemperaturePrimaryCircuit(self):
        return self.service.getProperty("heating.primaryCircuit.sensors.temperature.return")["properties"]["value"]["value"]


class Compressor(DeviceWithComponent):

    @property
    def compressor(self) -> str:
        return self.component

    @handleNotSupported
    def getCompressorStarts(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["starts"]["value"]

    @handleNotSupported
    def getCompressorHours(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hours"]["value"]

    @handleNotSupported
    def getCompressorHoursLoadClass1(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassOne"]["value"]

    @handleNotSupported
    def getCompressorHoursLoadClass2(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassTwo"]["value"]

    @handleNotSupported
    def getCompressorHoursLoadClass3(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassThree"]["value"]

    @handleNotSupported
    def getCompressorHoursLoadClass4(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassFour"]["value"]

    @handleNotSupported
    def getCompressorHoursLoadClass5(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassFive"]["value"]

    @handleNotSupported
    def getCompressorActive(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}")["properties"]["active"]["value"]
