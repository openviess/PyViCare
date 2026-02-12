from __future__ import annotations
from contextlib import suppress
from typing import Any, List
from deprecated import deprecated

from PyViCare.PyViCareHeatingDevice import HeatingDevice, HeatingDeviceWithComponent
from PyViCare.PyViCareUtils import (PyViCareNotSupportedFeatureError,
                                    handleAPICommandErrors, handleNotSupported)
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

    @property
    def inverters(self) -> List[Inverter]:
        return [self.getInverter(x) for x in self.getAvailableCompressors()]

    def getInverter(self, inverter) -> Inverter:
        return Inverter(self, inverter)

    @handleNotSupported
    def getBufferMainTemperature(self):
        return self.getProperty("heating.bufferCylinder.sensors.temperature.main")["properties"]["value"]["value"]

    @handleNotSupported
    def getBufferTopTemperature(self):
        return self.getProperty("heating.bufferCylinder.sensors.temperature.top")["properties"]["value"]["value"]

    # Power consumption for Heating:
    @handleNotSupported
    def getPowerConsumptionHeatingUnit(self):
        return self.getProperty("heating.power.consumption.heating")["properties"]["day"]["unit"]

    @handleNotSupported
    def getPowerConsumptionHeatingToday(self):
        return self.getProperty("heating.power.consumption.heating")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionHeatingThisMonth(self):
        return self.getProperty("heating.power.consumption.heating")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionHeatingThisYear(self):
        return self.getProperty("heating.power.consumption.heating")["properties"]["year"]["value"][0]

    # Power summary consumption for Heating:
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

    # Total power consumption:
    @handleNotSupported
    def getPowerConsumptionUnit(self):
        return self.getProperty("heating.power.consumption.total")["properties"]["day"]["unit"]

    @handleNotSupported
    def getPowerConsumptionToday(self):
        return self.getProperty("heating.power.consumption.total")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionThisMonth(self):
        return self.getProperty("heating.power.consumption.total")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionThisYear(self):
        return self.getProperty("heating.power.consumption.total")["properties"]["year"]["value"][0]

    # Power consumption for Domestic Hot Water:
    @handleNotSupported
    def getPowerConsumptionDomesticHotWaterUnit(self):
        return self.getProperty("heating.power.consumption.dhw")["properties"]["day"]["unit"]

    @handleNotSupported
    def getPowerConsumptionDomesticHotWaterToday(self):
        return self.getProperty("heating.power.consumption.dhw")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionDomesticHotWaterThisMonth(self):
        return self.getProperty("heating.power.consumption.dhw")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionDomesticHotWaterThisYear(self):
        return self.getProperty("heating.power.consumption.dhw")["properties"]["year"]["value"][0]

    # Power summary consumption for Domestic Hot Water:
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

    # COP (Coefficient of Performance) - instantaneous efficiency metrics
    # Some devices expose COP instead of SPF
    @handleNotSupported
    def getCoefficientOfPerformanceHeating(self) -> float:
        return float(self.getProperty("heating.cop.heating")["properties"]["value"]["value"])

    @handleNotSupported
    def getCoefficientOfPerformanceDHW(self) -> float:
        return float(self.getProperty("heating.cop.dhw")["properties"]["value"]["value"])

    @handleNotSupported
    def getCoefficientOfPerformanceTotal(self) -> float:
        return float(self.getProperty("heating.cop.total")["properties"]["value"]["value"])

    @handleNotSupported
    def getCoefficientOfPerformanceCooling(self) -> float:
        return float(self.getProperty("heating.cop.cooling")["properties"]["value"]["value"])

    @property
    def heatingRod(self) -> HeatingRod:
        return HeatingRod(self)

    # Additional pressure sensors (refrigerant circuit)
    @handleNotSupported
    def getHotGasPressure(self) -> float:
        return float(self.getProperty("heating.sensors.pressure.hotGas")["properties"]["value"]["value"])

    @handleNotSupported
    def getHotGasPressureUnit(self) -> str:
        return str(self.getProperty("heating.sensors.pressure.hotGas")["properties"]["value"]["unit"])

    @handleNotSupported
    def getSuctionGasPressure(self) -> float:
        return float(self.getProperty("heating.sensors.pressure.suctionGas")["properties"]["value"]["value"])

    @handleNotSupported
    def getSuctionGasPressureUnit(self) -> str:
        return str(self.getProperty("heating.sensors.pressure.suctionGas")["properties"]["value"]["unit"])

    # Additional temperature sensors (refrigerant circuit)
    @handleNotSupported
    def getHotGasTemperature(self) -> float:
        return float(self.getProperty("heating.sensors.temperature.hotGas")["properties"]["value"]["value"])

    @handleNotSupported
    def getHotGasTemperatureUnit(self) -> str:
        return str(self.getProperty("heating.sensors.temperature.hotGas")["properties"]["value"]["unit"])

    @handleNotSupported
    def getLiquidGasTemperature(self) -> float:
        return float(self.getProperty("heating.sensors.temperature.liquidGas")["properties"]["value"]["value"])

    @handleNotSupported
    def getLiquidGasTemperatureUnit(self) -> str:
        return str(self.getProperty("heating.sensors.temperature.liquidGas")["properties"]["value"]["unit"])

    @handleNotSupported
    def getSuctionGasTemperature(self) -> float:
        return float(self.getProperty("heating.sensors.temperature.suctionGas")["properties"]["value"]["value"])

    @handleNotSupported
    def getSuctionGasTemperatureUnit(self) -> str:
        return str(self.getProperty("heating.sensors.temperature.suctionGas")["properties"]["value"]["unit"])

    # Main ECU runtime
    @handleNotSupported
    def getMainECURuntime(self) -> int:
        return int(self.getProperty("heating.device.mainECU")["properties"]["runtime"]["value"])

    @handleNotSupported
    def getMainECURuntimeUnit(self) -> str:
        return str(self.getProperty("heating.device.mainECU")["properties"]["runtime"]["unit"])

    # Configuration values
    @handleNotSupported
    def getConfigurationBufferTemperatureMax(self) -> float:
        return float(self.getProperty("heating.configuration.buffer.temperature.max")["properties"]["value"]["value"])

    @handleNotSupported
    def getConfigurationBufferTemperatureMaxUnit(self) -> str:
        return str(self.getProperty("heating.configuration.buffer.temperature.max")["properties"]["value"]["unit"])

    @handleNotSupported
    def getConfigurationOutsideTemperatureDampingFactor(self) -> int:
        return int(self.getProperty("heating.configuration.temperature.outside.DampingFactor")["properties"]["value"]["value"])

    @handleNotSupported
    def getConfigurationOutsideTemperatureDampingFactorUnit(self) -> str:
        return str(self.getProperty("heating.configuration.temperature.outside.DampingFactor")["properties"]["value"]["unit"])

    @handleNotSupported
    def getConfigurationHeatingRodDHWApproved(self) -> bool:
        return bool(self.getProperty("heating.configuration.heatingRod.dhw")["properties"]["useApproved"]["value"])

    @handleNotSupported
    def getConfigurationHeatingRodHeatingApproved(self) -> bool:
        return bool(self.getProperty("heating.configuration.heatingRod.heating")["properties"]["useApproved"]["value"])

    @handleNotSupported
    def getConfigurationDHWHeaterApproved(self) -> bool:
        return bool(self.getProperty("heating.configuration.dhwHeater")["properties"]["useApproved"]["value"])

    # Cooling circuits
    @property
    def coolingCircuits(self) -> List[CoolingCircuit]:
        return [self.getCoolingCircuit(x) for x in self.getAvailableCoolingCircuits()]

    def getCoolingCircuit(self, circuit) -> CoolingCircuit:
        return CoolingCircuit(self, circuit)

    def getAvailableCoolingCircuits(self):
        """Detect available cooling circuits (0, 1, 2, etc.)."""
        available = []
        for circuit in ['0', '1', '2', '3']:
            with suppress(KeyError, PyViCareNotSupportedFeatureError):
                if self.getProperty(f"heating.coolingCircuits.{circuit}.type") is not None:
                    available.append(circuit)
        return available


class CoolingCircuit(HeatingDeviceWithComponent):
    """Cooling circuit component for heat pumps with cooling capability."""

    @property
    def circuit(self) -> str:
        return self.component

    @handleNotSupported
    def getType(self) -> str:
        return str(self.getProperty(f"heating.coolingCircuits.{self.circuit}.type")["properties"]["value"]["value"])

    @handleNotSupported
    def getReverseActive(self) -> bool:
        return bool(self.getProperty(f"heating.coolingCircuits.{self.circuit}.reverse")["properties"]["active"]["value"])



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

    def getHoursLoadClass1(self):
        """Get hours in load class 1. Tries 'statistics' path first, then 'statistics.load'."""
        with suppress(KeyError):
            return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassOne"]["value"]
        with suppress(KeyError):
            return self.getProperty(f"heating.compressors.{self.compressor}.statistics.load")["properties"]["hoursLoadClassOne"]["value"]
        raise PyViCareNotSupportedFeatureError("getHoursLoadClass1")

    def getHoursLoadClass2(self):
        """Get hours in load class 2. Tries 'statistics' path first, then 'statistics.load'."""
        with suppress(KeyError):
            return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassTwo"]["value"]
        with suppress(KeyError):
            return self.getProperty(f"heating.compressors.{self.compressor}.statistics.load")["properties"]["hoursLoadClassTwo"]["value"]
        raise PyViCareNotSupportedFeatureError("getHoursLoadClass2")

    def getHoursLoadClass3(self):
        """Get hours in load class 3. Tries 'statistics' path first, then 'statistics.load'."""
        with suppress(KeyError):
            return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassThree"]["value"]
        with suppress(KeyError):
            return self.getProperty(f"heating.compressors.{self.compressor}.statistics.load")["properties"]["hoursLoadClassThree"]["value"]
        raise PyViCareNotSupportedFeatureError("getHoursLoadClass3")

    def getHoursLoadClass4(self):
        """Get hours in load class 4. Tries 'statistics' path first, then 'statistics.load'."""
        with suppress(KeyError):
            return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassFour"]["value"]
        with suppress(KeyError):
            return self.getProperty(f"heating.compressors.{self.compressor}.statistics.load")["properties"]["hoursLoadClassFour"]["value"]
        raise PyViCareNotSupportedFeatureError("getHoursLoadClass4")

    def getHoursLoadClass5(self):
        """Get hours in load class 5. Tries 'statistics' path first, then 'statistics.load'."""
        with suppress(KeyError):
            return self.getProperty(f"heating.compressors.{self.compressor}.statistics")["properties"]["hoursLoadClassFive"]["value"]
        with suppress(KeyError):
            return self.getProperty(f"heating.compressors.{self.compressor}.statistics.load")["properties"]["hoursLoadClassFive"]["value"]
        raise PyViCareNotSupportedFeatureError("getHoursLoadClass5")

    @handleNotSupported
    def getActive(self):
        return self.getProperty(f"heating.compressors.{self.compressor}")["properties"]["active"]["value"]

    @handleNotSupported
    def getPhase(self):
        return self.getProperty(f"heating.compressors.{self.compressor}")["properties"]["phase"]["value"]

    @handleNotSupported
    def getPower(self) -> float:
        # Returns the nominal/maximum power of the compressor in kW
        return float(self.getProperty(f"heating.compressors.{self.compressor}.power")["properties"]["value"]["value"])

    @handleNotSupported
    def getPowerUnit(self) -> str:
        return str(self.getProperty(f"heating.compressors.{self.compressor}.power")["properties"]["value"]["unit"])

    @handleNotSupported
    def getModulation(self) -> int:
        # Returns the current compressor modulation/power level as percentage (0-100)
        return int(self.getProperty(f"heating.compressors.{self.compressor}.sensors.power")["properties"]["value"]["value"])

    @handleNotSupported
    def getModulationUnit(self) -> str:
        return str(self.getProperty(f"heating.compressors.{self.compressor}.sensors.power")["properties"]["value"]["unit"])

    @handleNotSupported
    def getSpeed(self) -> int:
        return int(self.getProperty(f"heating.compressors.{self.compressor}.speed.current")["properties"]["value"]["value"])

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

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getOutletPressureUnit", version="2.55.1")
    def getCompressorOutletPressureUnit(self) -> str:
        return str(self.getOutletPressureUnit())

    @handleNotSupported
    def getOutletPressureUnit(self) -> str:
        # Shows the unit of measurement of the outlet pressure.
        return str(self.getProperty(f"heating.compressors.{self.compressor}.sensors.pressure.outlet")["properties"]["value"]["unit"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getOutletPressure", version="2.55.1")
    def getCompressorOutletPressure(self) -> float:
        return float(self.getOutletPressure())

    @handleNotSupported
    def getOutletPressure(self) -> float:
        # Shows the outlet pressure of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.pressure.outlet")["properties"]["value"]["value"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getInletPressureUnit", version="2.55.1")
    def getCompressorInletPressureUnit(self) -> str:
        return str(self.getInletPressureUnit())

    @handleNotSupported
    def getInletPressureUnit(self) -> str:
        # Shows the unit of measurement of the inlet pressure.
        return str(self.getProperty(f"heating.compressors.{self.compressor}.sensors.pressure.inlet")["properties"]["value"]["unit"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getInletPressure", version="2.55.1")
    def getCompressorInletPressure(self) -> float:
        return float(self.getInletPressure())

    @handleNotSupported
    def getInletPressure(self) -> float:
        # Shows the inlet pressure of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.pressure.inlet")["properties"]["value"]["value"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getOutletTemperatureUnit", version="2.55.1")
    def getCompressorOutletTemperatureUnit(self) -> str:
        return str(self.getOutletTemperatureUnit())

    @handleNotSupported
    def getOutletTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the outlet temperature.
        return str(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.outlet")["properties"]["value"]["unit"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getOutletTemperature", version="2.55.1")
    def getCompressorOutletTemperature(self) -> float:
        return float(self.getOutletTemperature())

    @handleNotSupported
    def getOutletTemperature(self) -> float:
        # Shows the outlet temperature of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.outlet")["properties"]["value"]["value"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getInletTemperatureUnit", version="2.55.1")
    def getCompressorInletTemperatureUnit(self) -> str:
        return str(self.getInletTemperatureUnit())

    @handleNotSupported
    def getInletTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the inlet temperature.
        return str(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.inlet")["properties"]["value"]["unit"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getInletTemperature", version="2.55.1")
    def getCompressorInletTemperature(self) -> float:
        return float(self.getInletTemperature())

    @handleNotSupported
    def getInletTemperature(self) -> float:
        # Shows the inlet temperature of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.inlet")["properties"]["value"]["value"])

    @handleNotSupported
    def getOilTemperature(self) -> float:
        # Shows the oil temperature of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.oil")["properties"]["value"]["value"])

    def getMotorChamberTemperature(self) -> float:
        # Shows the motor chamber temperature of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.motorChamber")["properties"]["value"]["value"])

    def getAmbientTemperature(self) -> float:
        # Shows the ambient temperature of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.ambient")["properties"]["value"]["value"])

    def getOverheatTemperature(self) -> float:
        # Shows the overheat temperature of the compressor.
        return float(self.getProperty(f"heating.compressors.{self.compressor}.sensors.temperature.overheat")["properties"]["value"]["value"])


class Evaporator(HeatingDeviceWithComponent):

    @property
    def evaporator(self) -> str:
        return self.component

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getLiquidTemperatureUnit", version="2.55.1")
    def getEvaporatorLiquidTemperatureUnit(self) -> str:
        return str(self.getLiquidTemperatureUnit())

    @handleNotSupported
    def getLiquidTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the liquid temperature of the evaporator.
        return str(self.getProperty(f"heating.evaporators.{self.evaporator}.sensors.temperature.liquid")["properties"]["value"]["unit"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getLiquidTemperature", version="2.55.1")
    def getEvaporatorLiquidTemperature(self) -> float:
        return float(self.getLiquidTemperature())

    @handleNotSupported
    def getLiquidTemperature(self) -> float:
        # Shows the liquid temperature of the evaporator.
        return float(self.getProperty(f"heating.evaporators.{self.evaporator}.sensors.temperature.liquid")["properties"]["value"]["value"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getOverheatTemperatureUnit", version="2.55.1")
    def getEvaporatorOverheatTemperatureUnit(self) -> str:
        return str(self.getOverheatTemperatureUnit())

    @handleNotSupported
    def getOverheatTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the overheat temperature of the evaporator.
        return str(self.getProperty(f"heating.evaporators.{self.evaporator}.sensors.temperature.overheat")["properties"]["value"]["unit"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getOverheatTemperature", version="2.55.1")
    def getEvaporatorOverheatTemperature(self) -> float:
        return float(self.getOverheatTemperature())

    @handleNotSupported
    def getOverheatTemperature(self) -> float:
        # Shows the overheat temperature of the evaporator.
        return float(self.getProperty(f"heating.evaporators.{self.evaporator}.sensors.temperature.overheat")["properties"]["value"]["value"])


class Condensor(HeatingDeviceWithComponent):

    @property
    def condensor(self) -> str:
        return self.component

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getSubcoolingTemperatureUnit", version="2.55.1")
    def getCondensorSubcoolingTemperatureUnit(self) -> str:
        return str(self.getSubcoolingTemperatureUnit())

    @handleNotSupported
    def getSubcoolingTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the subcooling temperature of the condenser.
        return str(self.getProperty(f"heating.condensors.{self.condensor}.sensors.temperature.subcooling")["properties"]["value"]["unit"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getSubcoolingTemperature", version="2.55.1")
    def getCondensorSubcoolingTemperature(self) -> float:
        return float(self.getSubcoolingTemperature())

    @handleNotSupported
    def getSubcoolingTemperature(self) -> float:
        # Shows the subcooling temperature of the condenser.
        return float(self.getProperty(f"heating.condensors.{self.condensor}.sensors.temperature.subcooling")["properties"]["value"]["value"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getLiquidTemperatureUnit", version="2.55.1")
    def getCondensorLiquidTemperatureUnit(self) -> str:
        return str(self.getLiquidTemperatureUnit())

    @handleNotSupported
    def getLiquidTemperatureUnit(self) -> str:
        # Shows the unit of measurement of the liquid temperature of the condenser.
        return str(self.getProperty(f"heating.condensors.{self.condensor}.sensors.temperature.liquid")["properties"]["value"]["unit"])

    #TODO: remove deprecated method in 03.2026 release
    @handleNotSupported
    @deprecated(reason="renamed, use getLiquidTemperature", version="2.55.1")
    def getCondensorLiquidTemperature(self) -> float:
        return float(self.getLiquidTemperature())

    @handleNotSupported
    def getLiquidTemperature(self) -> float:
        # Shows the liquid temperature of the condenser.
        return float(self.getProperty(f"heating.condensors.{self.condensor}.sensors.temperature.liquid")["properties"]["value"]["value"])


class Inverter(HeatingDeviceWithComponent):

    @property
    def inverter(self) -> str:
        return self.component

    @handleNotSupported
    def getCurrent(self) -> float:
        return float(self.getProperty(f"heating.inverters.{self.inverter}.sensors.power.current")["properties"]["value"]["value"])

    @handleNotSupported
    def getPower(self) -> float:
        return float(self.getProperty(f"heating.inverters.{self.inverter}.sensors.power.output")["properties"]["value"]["value"])

    @handleNotSupported
    def getTemperature(self) -> float:
        return float(self.getProperty(f"heating.inverters.{self.inverter}.sensors.temperature.powerModule")["properties"]["value"]["value"])


class HeatingRod:

    def __init__(self, device: HeatPump) -> None:
        self.service = device.service

    def getProperty(self, property_name: str) -> Any:
        return self.service.getProperty(property_name)

    @handleNotSupported
    def getStarts(self) -> int:
        return int(self.getProperty("heating.heatingRod.statistics")["properties"]["starts"]["value"])

    @handleNotSupported
    def getHours(self) -> int:
        return int(self.getProperty("heating.heatingRod.statistics")["properties"]["hours"]["value"])

    @handleNotSupported
    def getHeatProductionCurrent(self) -> float:
        return float(self.getProperty("heating.heatingRod.heat.production.current")["properties"]["value"]["value"])

    @handleNotSupported
    def getHeatProductionCurrentUnit(self) -> str:
        return str(self.getProperty("heating.heatingRod.heat.production.current")["properties"]["value"]["unit"])

    @handleNotSupported
    def getPowerConsumptionCurrent(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.current")["properties"]["value"]["value"])

    @handleNotSupported
    def getPowerConsumptionCurrentUnit(self) -> str:
        return str(self.getProperty("heating.heatingRod.power.consumption.current")["properties"]["value"]["unit"])

    @handleNotSupported
    def getPowerConsumptionDHWThisYear(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.dhw")["properties"]["year"]["value"][0])

    @handleNotSupported
    def getPowerConsumptionHeatingThisYear(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.heating")["properties"]["year"]["value"][0])

    @handleNotSupported
    def getPowerConsumptionTotalThisYear(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.total")["properties"]["year"]["value"][0])

    # Power consumption summary for DHW:
    @handleNotSupported
    def getPowerConsumptionSummaryDHWUnit(self) -> str:
        return str(self.getProperty("heating.heatingRod.power.consumption.summary.dhw")["properties"]["currentDay"]["unit"])

    @handleNotSupported
    def getPowerConsumptionSummaryDHWCurrentDay(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.dhw")["properties"]["currentDay"]["value"])

    @handleNotSupported
    def getPowerConsumptionSummaryDHWCurrentMonth(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.dhw")["properties"]["currentMonth"]["value"])

    @handleNotSupported
    def getPowerConsumptionSummaryDHWCurrentYear(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.dhw")["properties"]["currentYear"]["value"])

    @handleNotSupported
    def getPowerConsumptionSummaryDHWLastMonth(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.dhw")["properties"]["lastMonth"]["value"])

    @handleNotSupported
    def getPowerConsumptionSummaryDHWLastSevenDays(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.dhw")["properties"]["lastSevenDays"]["value"])

    @handleNotSupported
    def getPowerConsumptionSummaryDHWLastYear(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.dhw")["properties"]["lastYear"]["value"])

    # Power consumption summary for Heating:
    @handleNotSupported
    def getPowerConsumptionSummaryHeatingUnit(self) -> str:
        return str(self.getProperty("heating.heatingRod.power.consumption.summary.heating")["properties"]["currentDay"]["unit"])

    @handleNotSupported
    def getPowerConsumptionSummaryHeatingCurrentDay(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.heating")["properties"]["currentDay"]["value"])

    @handleNotSupported
    def getPowerConsumptionSummaryHeatingCurrentMonth(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.heating")["properties"]["currentMonth"]["value"])

    @handleNotSupported
    def getPowerConsumptionSummaryHeatingCurrentYear(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.heating")["properties"]["currentYear"]["value"])

    @handleNotSupported
    def getPowerConsumptionSummaryHeatingLastMonth(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.heating")["properties"]["lastMonth"]["value"])

    @handleNotSupported
    def getPowerConsumptionSummaryHeatingLastSevenDays(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.heating")["properties"]["lastSevenDays"]["value"])

    @handleNotSupported
    def getPowerConsumptionSummaryHeatingLastYear(self) -> float:
        return float(self.getProperty("heating.heatingRod.power.consumption.summary.heating")["properties"]["lastYear"]["value"])

    # Runtime by level
    @handleNotSupported
    def getRuntimeLevelOne(self) -> int:
        return int(self.getProperty("heating.heatingRod.runtime")["properties"]["levelOne"]["value"])

    @handleNotSupported
    def getRuntimeLevelTwo(self) -> int:
        return int(self.getProperty("heating.heatingRod.runtime")["properties"]["levelTwo"]["value"])

    @handleNotSupported
    def getRuntimeLevelOneUnit(self) -> str:
        return str(self.getProperty("heating.heatingRod.runtime")["properties"]["levelOne"]["unit"])
