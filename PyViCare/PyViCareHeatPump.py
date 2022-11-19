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
        return self.service.getProperty("heating.compressors")["properties"]["enabled"]["value"]

    @handleNotSupported
    def getBufferMainTemperature(self):
        return self.service.getProperty("heating.buffer.sensors.temperature.main")["properties"]['value']['value']

    @handleNotSupported
    def getBufferTopTemperature(self):
        return self.service.getProperty("heating.buffer.sensors.temperature.top")["properties"]['value']['value']


class Compressor(DeviceWithComponent):

    @property
    def compressor(self) -> str:
        return self.component

    @handleNotSupported
    def getStarts(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["starts"]["value"]

    @handleNotSupported
    def getHours(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hours"]["value"]

    @handleNotSupported
    def getHoursLoadClass1(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassOne"]["value"]

    @handleNotSupported
    def getHoursLoadClass2(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassTwo"]["value"]

    @handleNotSupported
    def getHoursLoadClass3(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassThree"]["value"]

    @handleNotSupported
    def getHoursLoadClass4(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassFour"]["value"]

    @handleNotSupported
    def getHoursLoadClass5(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassFive"]["value"]

    @handleNotSupported
    def getActive(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}")["properties"]["active"]["value"]

    @handleNotSupported
    def getPowerConsumptionToday(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionDomesticHotWaterToday(self):
        return self.service.getProperty("heating.power.consumption.dhw")["properties"]["day"]["value"][0]
