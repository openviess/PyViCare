from PyViCare.PyViCareDevice import Device, DeviceWithCircuit
from PyViCare.PyViCareUtils import handleNotSupported


class GazBoiler(Device):

    def getCircuit(self, circuit):
        return GazBoilerWithCircuit(self, circuit)

    @handleNotSupported
    def getBurnerActive(self):
        return self.service.getProperty("heating.burner")["properties"]["active"]["value"]

    @handleNotSupported
    def getGasConsumptionHeatingDays(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["day"]["value"]

    @handleNotSupported
    def getGasConsumptionHeatingToday(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getGasConsumptionHeatingWeeks(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["week"]["value"]

    @handleNotSupported
    def getGasConsumptionHeatingThisWeek(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["week"]["value"][0]

    @handleNotSupported
    def getGasConsumptionHeatingMonths(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["month"]["value"]

    @handleNotSupported
    def getGasConsumptionHeatingThisMonth(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getGasConsumptionHeatingYears(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["year"]["value"]

    @handleNotSupported
    def getGasConsumptionHeatingThisYear(self):
        return self.service.getProperty("heating.gas.consumption.heating")["properties"]["year"]["value"][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterDays(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["day"]["value"]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterToday(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterWeeks(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["week"]["value"]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterThisWeek(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["week"]["value"][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterMonths(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["month"]["value"]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterThisMonth(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterYears(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["year"]["value"]

    @handleNotSupported
    def getGasConsumptionDomesticHotWaterThisYear(self):
        return self.service.getProperty("heating.gas.consumption.dhw")["properties"]["year"]["value"][0]

    @handleNotSupported
    def getBoilerTemperature(self):
        return self.service.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]

    @handleNotSupported
    def getPowerConsumptionDays(self):
        return self.service.getProperty("heating.power.consumption")["properties"]["day"]["value"]

    @handleNotSupported
    def getPowerConsumptionToday(self):
        return self.service.getProperty("heating.power.consumption")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionWeeks(self):
        return self.service.getProperty("heating.power.consumption")["properties"]["week"]["value"]

    @handleNotSupported
    def getPowerConsumptionThisWeek(self):
        return self.service.getProperty("heating.power.consumption")["properties"]["week"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionMonths(self):
        return self.service.getProperty("heating.power.consumption")["properties"]["month"]["value"]

    @handleNotSupported
    def getPowerConsumptionThisMonth(self):
        return self.service.getProperty("heating.power.consumption")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionYears(self):
        return self.service.getProperty("heating.power.consumption")["properties"]["year"]["value"]

    @handleNotSupported
    def getPowerConsumptionThisYear(self):
        return self.service.getProperty("heating.power.consumption")["properties"]["year"]["value"][0]


class GazBoilerWithCircuit(DeviceWithCircuit):

    @handleNotSupported
    def getBurnerHours(self):
        return self.service.getProperty(f"heating.burners.{self.circuit}.statistics")["properties"]["hours"]["value"]

    @handleNotSupported
    def getBurnerStarts(self):
        return self.service.getProperty(f"heating.burners.{self.circuit}.statistics")["properties"]["starts"]["value"]

    @handleNotSupported
    def getBurnerModulation(self):
        return self.service.getProperty(f"heating.burners.{self.circuit}.modulation")["properties"]["value"]["value"]
