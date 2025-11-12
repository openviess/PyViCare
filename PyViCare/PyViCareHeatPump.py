from __future__ import annotations
from typing import Any, List
from deprecated import deprecated

from PyViCare.PyViCareHeatingDevice import HeatingDevice, HeatingDeviceWithComponent
from PyViCare.PyViCareUtils import handleAPICommandErrors, handleNotSupported
from PyViCare.PyViCareVentilationDevice import VentilationDevice


class HeatPump(HeatingDevice, VentilationDevice):

    @property
    def compressors(self) -> List[Compressor]:
        return [self.getCompressor(x) for x in self.getAvailableCompressors()]

    def getCompressor(self, compressor) -> Compressor:
        return Compressor(self, compressor)

    @handleNotSupported
    def getAvailableCompressors(self):
        return self.getProperty("heating.compressors")["properties"]["enabled"]["value"]

    @property
    def condensors(self) -> List[Condensor]:
        return [self.getCondensor(x) for x in self.getAvailableCompressors()]

    def getCondensor(self, condensor) -> Condensor:
        return Condensor(self, condensor)

    @property
    def evaporators(self) -> List[Evaporator]:
        return [self.getEvaporator(x) for x in self.getAvailableCompressors()]

    def getEvaporator(self, evaporator) -> Evaporator:
        return Evaporator(self, evaporator)

    @handleNotSupported
    def getBufferMainTemperature(self):
        return self.getProperty("heating.bufferCylinder.sensors.temperature.main")["properties"]['value']['value']

    @handleNotSupported
    def getBufferTopTemperature(self):
        return self.getProperty("heating.bufferCylinder.sensors.temperature.top")["properties"]['value']['value']

    # Power consumption for Heating:
    @handleNotSupported
    def getPowerSummaryConsumptionHeatingUnit(self):
        return self.getProperty("heating.power.consumption.summary.heating")["properties"]["currentDay"]["unit"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingCurrentDay(self):
        return self.getProperty("heating.power.consumption.summary.heating")["properties"]["currentDay"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingCurrentMonth(self):
        return self.getProperty("heating.power.consumption.summary.heating")["properties"]["currentMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingCurrentYear(self):
        return self.getProperty("heating.power.consumption.summary.heating")["properties"]["currentYear"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingLastMonth(self):
        return self.getProperty("heating.power.consumption.summary.heating")["properties"]["lastMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingLastSevenDays(self):
        return self.getProperty("heating.power.consumption.summary.heating")["properties"]["lastSevenDays"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingLastYear(self):
        return self.getProperty("heating.power.consumption.summary.heating")["properties"]["lastYear"]["value"]

    # Power consumption for Cooling:
    @handleNotSupported
    def getPowerConsumptionCoolingUnit(self):
        return self.getProperty("heating.power.consumption.cooling")["properties"]["day"]["unit"]

    @handleNotSupported
    def getPowerConsumptionCoolingToday(self):
        return self.getProperty("heating.power.consumption.cooling")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionCoolingThisMonth(self):
        return self.getProperty("heating.power.consumption.cooling")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionCoolingThisYear(self):
        return self.getProperty("heating.power.consumption.cooling")["properties"]["year"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionUnit(self):
        return self.getProperty("heating.power.consumption.total")["properties"]["day"]["unit"]

    @handleNotSupported
    def getPowerConsumptionToday(self):
        return self.getProperty("heating.power.consumption.total")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionDomesticHotWaterToday(self):
        return self.getProperty("heating.power.consumption.dhw")["properties"]["day"]["value"][0]

    # Power consumption for Domestic Hot Water:
    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterUnit(self):
        return self.getProperty("heating.power.consumption.summary.dhw")["properties"]["currentDay"]["unit"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterCurrentDay(self):
        return self.getProperty("heating.power.consumption.summary.dhw")["properties"]["currentDay"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(self):
        return self.getProperty("heating.power.consumption.summary.dhw")["properties"]["currentMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterCurrentYear(self):
        return self.getProperty("heating.power.consumption.summary.dhw")["properties"]["currentYear"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterLastMonth(self):
        return self.getProperty("heating.power.consumption.summary.dhw")["properties"]["lastMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(self):
        return self.getProperty("heating.power.consumption.summary.dhw")["properties"]["lastSevenDays"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterLastYear(self):
        return self.getProperty("heating.power.consumption.summary.dhw")["properties"]["lastYear"]["value"]

    @handleNotSupported
    def getVolumetricFlowReturn(self):
        return self.getProperty("heating.sensors.volumetricFlow.allengra")["properties"]['value']['value']

    @handleNotSupported
    @deprecated(reason="renamed, use getVentilationModes", version="2.40.0")
    def getAvailableVentilationModes(self):
        return self.getVentilationModes()

    @deprecated(reason="renamed, use activateVentilationMode", version="2.40.0")
    def setActiveVentilationMode(self, mode):
        """ Set the active mode
        Parameters
        ----------
        mode : str
            Valid mode can be obtained using getModes()

        Returns
        -------
        result: json
            json representation of the answer
        """
        return self.activateVentilationMode(mode)

    @handleNotSupported
    @deprecated(reason="renamed, use getVentilationPrograms", version="2.40.0")
    def getAvailableVentilationPrograms(self):
        return self.getVentilationPrograms()

    @handleNotSupported
    def getDomesticHotWaterHysteresisUnit(self) -> str:
        return str(self.getProperty("heating.dhw.temperature.hysteresis")["properties"]["value"]["unit"])

    @handleNotSupported
    def getDomesticHotWaterHysteresis(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["properties"]["value"]["value"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisMin(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresis"]["params"]["hysteresis"]["constraints"]["min"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisMax(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresis"]["params"]["hysteresis"]["constraints"]["max"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisStepping(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresis"]["params"]["hysteresis"]["constraints"]["stepping"])

    @handleAPICommandErrors
    def setDomesticHotWaterHysteresis(self, temperature: float) -> Any:
        """ Set the hysteresis temperature for domestic host water
        Parameters
        ----------
        temperature : float
            hysteresis temperature

        Returns
        -------
        result: json
            json representation of the answer
        """
        return self.setProperty("heating.dhw.temperature.hysteresis", "setHysteresis", {'hysteresis': temperature})

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOn(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["properties"]["switchOnValue"]["value"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOnMin(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOnValue"]["params"]["hysteresis"]["constraints"]["min"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOnMax(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOnValue"]["params"]["hysteresis"]["constraints"]["max"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOnStepping(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOnValue"]["params"]["hysteresis"]["constraints"]["stepping"])

    @handleAPICommandErrors
    def setDomesticHotWaterHysteresisSwitchOn(self, temperature: float) -> Any:
        """ Set the hysteresis switch on temperature for domestic host water
        Parameters
        ----------
        temperature : float
            hysteresis switch on temperature

        Returns
        -------
        result: json
            json representation of the answer
        """
        return self.setProperty("heating.dhw.temperature.hysteresis", "setHysteresisSwitchOnValue", {'hysteresis': temperature})

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOff(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["properties"]["switchOffValue"]["value"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOffMin(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOffValue"]["params"]["hysteresis"]["constraints"]["min"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOffMax(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOffValue"]["params"]["hysteresis"]["constraints"]["max"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOffStepping(self) -> float:
        return float(self.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOffValue"]["params"]["hysteresis"]["constraints"]["stepping"])

    @handleAPICommandErrors
    def setDomesticHotWaterHysteresisSwitchOff(self, temperature: float) -> Any:
        """ Set the hysteresis switch off temperature for domestic host water
        Parameters
        ----------
        temperature : float
            hysteresis switch off temperature

        Returns
        -------
        result: json
            json representation of the answer
        """
        return self.setProperty("heating.dhw.temperature.hysteresis", "setHysteresisSwitchOffValue", {'hysteresis': temperature})

    @handleNotSupported
    def getSupplyPressureUnit(self) -> str:
        # Returns heating supply pressure unit (e.g. bar)
        return str(self.getProperty("heating.sensors.pressure.supply")["properties"]["value"]["unit"])

    @handleNotSupported
    def getSupplyPressure(self) -> float:
        # Returns heating supply pressure
        return float(self.getProperty("heating.sensors.pressure.supply")["properties"]["value"]["value"])

    @handleNotSupported
    def getSeasonalPerformanceFactorDHW(self) -> float:
        return float(self.getProperty("heating.spf.dhw")["properties"]["value"]["value"])

    @handleNotSupported
    def getSeasonalPerformanceFactorHeating(self) -> float:
        return float(self.getProperty("heating.spf.heating")["properties"]["value"]["value"])

    @handleNotSupported
    def getSeasonalPerformanceFactorTotal(self) -> float:
        return float(self.getProperty("heating.spf.total")["properties"]["value"]["value"])

    @handleNotSupported
    def getHeatingRodStarts(self) -> int:
        return int(self.getProperty("heating.heatingRod.statistics")["properties"]["starts"]["value"])

    @handleNotSupported
    def getHeatingRodHours(self) -> int:
        return int(self.getProperty("heating.heatingRod.statistics")["properties"]["hours"]["value"])

    @handleNotSupported
    def getHeatingRodHeatProductionCurrent(self) -> float:
        return float(self.getProperty("heating.heatingRod.heat.production.current")["properties"]["value"]["value"])

    @handleNotSupported
    def getHeatingRodHeatProductionCurrentUnit(self) -> str:
        return str(self.getProperty("heating.heatingRod.heat.production.current")["properties"]["value"]["unit"])

    @handleNotSupported
    def getHeatingRodPowerConsumptionCurrent(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.current")["properties"]["value"]["value"])

    @handleNotSupported
    def getHeatingRodPowerConsumptionCurrentUnit(self) -> str:
        return str(self.getProperty("heating.heatingRod.power.consumption.current")["properties"]["value"]["unit"])

    @handleNotSupported
    def getHeatingRodPowerConsumptionDHWThisYear(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.dhw")["properties"]["year"]["value"][0])

    @handleNotSupported
    def getHeatingRodPowerConsumptionHeatingThisYear(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.heating")["properties"]["year"]["value"][0])

    @handleNotSupported
    def getHeatingRodPowerConsumptionTotalThisYear(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.total")["properties"]["year"]["value"][0])


class Compressor(HeatingDeviceWithComponent):

    @property
    def compressor(self) -> str:
        return self.component

    @handleNotSupported
    def getStarts(self):
        return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["starts"]["value"]

    @handleNotSupported
    def getHours(self):
        return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hours"]["value"]

    @handleNotSupported
    def getHoursLoadClass1(self):
        return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassOne"]["value"]

    @handleNotSupported
    def getHoursLoadClass2(self):
        return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassTwo"]["value"]

    @handleNotSupported
    def getHoursLoadClass3(self):
        return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassThree"]["value"]

    @handleNotSupported
    def getHoursLoadClass4(self):
        return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassFour"]["value"]

    @handleNotSupported
    def getHoursLoadClass5(self):
        return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassFive"]["value"]

    @handleNotSupported
    def getActive(self):
        return self.getProperty(f"heating.compressors.{self.compressor}")["properties"]["active"]["value"]

    @handleNotSupported
    def getPhase(self):
        return self.getProperty(f"heating.compressors.{self.compressor}")["properties"]["phase"]["value"]

    @handleNotSupported
    def getHeatProductionCurrent(self) -> float:
        return float(self.getProperty(f"heating.compressors.{self.compressor}.heat.production.current")["properties"]["value"]["value"])

    @handleNotSupported
    def getHeatProductionCurrentUnit(self) -> str:
        return str(self.getProperty(f"heating.compressors.{self.compressor}.heat.production.current")["properties"]["value"]["unit"])

    @handleNotSupported
    def getPowerConsumptionCurrent(self) -> float:
        return float(self.getProperty(f"heating.compressors.{self.compressor}.power.consumption.current")["properties"]["value"]["value"])

    @handleNotSupported
    def getPowerConsumptionCurrentUnit(self) -> str:
        return str(self.getProperty(f"heating.compressors.{self.compressor}.power.consumption.current")["properties"]["value"]["unit"])

    @handleNotSupported
    def getPowerConsumptionDHWThisYear(self) -> float:
        return float(self.getProperty(f"heating.compressors.{self.compressor}.power.consumption.dhw")["properties"]["year"]["value"][0])

    @handleNotSupported
    def getPowerConsumptionHeatingThisYear(self) -> float:
        return float(self.getProperty(f"heating.compressors.{self.compressor}.power.consumption.heating")["properties"]["year"]["value"][0])

    @handleNotSupported
    def getPowerConsumptionCoolingThisYear(self) -> float:
        return float(self.getProperty(f"heating.compressors.{self.compressor}.power.consumption.cooling")["properties"]["year"]["value"][0])

    @handleNotSupported
    def getPowerConsumptionTotalThisYear(self) -> float:
        return float(self.getProperty(f"heating.compressors.{self.compressor}.power.consumption.total")["properties"]["year"]["value"][0])

    @handleNotSupported
    def getPowerConsumptionTotalUnit(self) -> str:
        return str(self.getProperty(f"heating.compressors.{self.compressor}.power.consumption.total")["properties"]["year"]["unit"])

    @handleNotSupported
    def getCompressorOutletPressureUnit(self) -> str:
        # Shows the unit of measurement of the outlet pressure.
        return str(self.getProperty(f"heating.compressors.{self.compressor}.sensors.pressure.outlet")["properties"]["value"]["unit"])

    @handleNotSupported
    def getCompressorOutletPressure(self) -> float:
        # Shows the outlet pressure of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.pressure.outlet")["properties"]["value"]["value"])

    @handleNotSupported
    def getCompressorInletPressureUnit(self) -> str:
        # Shows the unit of measurement of the inlet pressure.
        return str(self.getProperty(f"heating.compressors.{self.compressor}.sensors.pressure.inlet")["properties"]["value"]["unit"])

    @handleNotSupported
    def getCompressorInletPressure(self) -> float:
        # Shows the inlet pressure of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.pressure.inlet")["properties"]["value"]["value"])

    @handleNotSupported
    def getCompressorOutletTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the outlet temperature.
        return str(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.outlet")["properties"]["value"]["unit"])

    @handleNotSupported
    def getCompressorOutletTemperature(self) -> float:
        # Shows the outlet temperature of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.outlet")["properties"]["value"]["value"])

    @handleNotSupported
    def getCompressorInletTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the inlet temperature.
        return str(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.inlet")["properties"]["value"]["unit"])

    @handleNotSupported
    def getCompressorInletTemperature(self) -> float:
        # Shows the inlet temperature of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.inlet")["properties"]["value"]["value"])


class Evaporator(HeatingDeviceWithComponent):

    @property
    def evaporator(self) -> str:
        return self.component

    @handleNotSupported
    def getEvaporatorLiquidTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the liquid temperature of the evaporator.
        return str(self.getProperty(f"heating.evaporators.{self.evaporator}.sensors.temperature.liquid")["properties"]["value"]["unit"])

    @handleNotSupported
    def getEvaporatorLiquidTemperature(self) -> float:
        # Shows the liquid temperature of the evaporator.
        return float(self.getProperty(f"heating.evaporators.{self.evaporator}.sensors.temperature.liquid")["properties"]["value"]["value"])

    @handleNotSupported
    def getEvaporatorOverheatTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the overheat temperature of the evaporator.
        return str(self.getProperty(f"heating.evaporators.{self.evaporator}.sensors.temperature.overheat")["properties"]["value"]["unit"])

    @handleNotSupported
    def getEvaporatorOverheatTemperature(self) -> float:
        # Shows the overheat temperature of the evaporator.
        return float(self.getProperty(f"heating.evaporators.{self.evaporator}.sensors.temperature.overheat")["properties"]["value"]["value"])


class Condensor(HeatingDeviceWithComponent):

    @property
    def condensor(self) -> str:
        return self.component

    @handleNotSupported
    def getCondensorSubcoolingTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the subcooling temperature of the condensor.
        return str(self.getProperty(f"heating.condensors.{self.condensor}.sensors.temperature.subcooling")["properties"]["value"]["unit"])

    @handleNotSupported
    def getCondensorSubcoolingTemperature(self) -> float:
        # Shows the subcooling temperature of the condensor.
        return float(self.getProperty(f"heating.condensors.{self.condensor}.sensors.temperature.subcooling")["properties"]["value"]["value"])

    @handleNotSupported
    def getCondensorLiquidTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the liquid temperature of the condensor.
        return str(self.getProperty(f"heating.condensors.{self.condensor}.sensors.temperature.liquid")["properties"]["value"]["unit"])

    @handleNotSupported
    def getCondensorLiquidTemperature(self) -> float:
        # Shows the liquid temperature of the condensor.
        return float(self.getProperty(f"heating.condensors.{self.condensor}.sensors.temperature.liquid")["properties"]["value"]["value"])
