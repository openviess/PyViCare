from contextlib import suppress
from typing import Any, List

from PyViCare.PyViCareHeatingDevice import (HeatingDevice,
                                            HeatingDeviceWithComponent)
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError, handleAPICommandErrors, handleNotSupported


class HeatPump(HeatingDevice):

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
        return self.service.getProperty("heating.bufferCylinder.sensors.temperature.main")["properties"]['value']['value']

    @handleNotSupported
    def getBufferTopTemperature(self):
        return self.service.getProperty("heating.bufferCylinder.sensors.temperature.top")["properties"]['value']['value']

    # Power consumption for Heating:
    @handleNotSupported
    def getPowerSummaryConsumptionHeatingUnit(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["currentDay"]["unit"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingCurrentDay(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["currentDay"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingCurrentMonth(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["currentMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingCurrentYear(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["currentYear"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingLastMonth(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["lastMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingLastSevenDays(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["lastSevenDays"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionHeatingLastYear(self):
        return self.service.getProperty("heating.power.consumption.summary.heating")["properties"]["lastYear"]["value"]

    @handleNotSupported
    def getPowerConsumptionUnit(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["day"]["unit"]

    @handleNotSupported
    def getPowerConsumptionToday(self):
        return self.service.getProperty("heating.power.consumption.total")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getPowerConsumptionDomesticHotWaterToday(self):
        return self.service.getProperty("heating.power.consumption.dhw")["properties"]["day"]["value"][0]

    # Power consumption for Domestic Hot Water:
    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterUnit(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["currentDay"]["unit"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterCurrentDay(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["currentDay"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterCurrentMonth(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["currentMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterCurrentYear(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["currentYear"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterLastMonth(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["lastMonth"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterLastSevenDays(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["lastSevenDays"]["value"]

    @handleNotSupported
    def getPowerSummaryConsumptionDomesticHotWaterLastYear(self):
        return self.service.getProperty("heating.power.consumption.summary.dhw")["properties"]["lastYear"]["value"]

    @handleNotSupported
    def getVolumetricFlowReturn(self):
        return self.service.getProperty("heating.sensors.volumetricFlow.allengra")["properties"]['value']['value']

    @handleNotSupported
    def getAvailableVentilationModes(self):
        return self.service.getProperty("ventilation.operating.modes.active")["commands"]["setMode"]["params"]["mode"]["constraints"]["enum"]

    @handleNotSupported
    def getActiveVentilationMode(self):
        return self.service.getProperty("ventilation.operating.modes.active")["properties"]["value"]["value"]

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
        return self.service.setProperty("ventilation.operating.modes.active", "setMode", {'mode': mode})

    @handleNotSupported
    def getAvailableVentilationPrograms(self):
        available_programs = []
        for program in ['basic', 'intensive', 'reduced', 'standard', 'standby', 'holidayAtHome', 'permanent']:
            with suppress(PyViCareNotSupportedFeatureError):
                if self.service.getProperty(f"ventilation.operating.programs.{program}") is not None:
                    available_programs.append(program)
        return available_programs

    @handleNotSupported
    def getActiveVentilationProgram(self):
        return self.service.getProperty("ventilation.operating.programs.active")["properties"]["value"]["value"]

    def activateVentilationProgram(self, program):
        """ Activate a ventilation program
            NOTE
            DEVICE_COMMUNICATION_ERROR can just mean that the program is already on
        Parameters
        ----------
        program : str

        Returns
        -------
        result: json
            json representation of the answer
        """
        return self.service.setProperty(f"ventilation.operating.programs.{program}", "activate", {})

    @handleNotSupported
    def getDomesticHotWaterHysteresisUnit(self) -> str:
        return str(self.service.getProperty("heating.dhw.temperature.hysteresis")["properties"]["value"]["unit"])

    @handleNotSupported
    def getDomesticHotWaterHysteresis(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["properties"]["value"]["value"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisMin(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresis"]["params"]["hysteresis"]["constraints"]["min"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisMax(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresis"]["params"]["hysteresis"]["constraints"]["max"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisStepping(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresis"]["params"]["hysteresis"]["constraints"]["stepping"])

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
        return self.service.setProperty("heating.dhw.temperature.hysteresis", "setHysteresis", {'hysteresis': temperature})

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOn(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["properties"]["switchOnValue"]["value"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOnMin(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOnValue"]["params"]["hysteresis"]["constraints"]["min"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOnMax(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOnValue"]["params"]["hysteresis"]["constraints"]["max"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOnStepping(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOnValue"]["params"]["hysteresis"]["constraints"]["stepping"])

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
        return self.service.setProperty("heating.dhw.temperature.hysteresis", "setHysteresisSwitchOnValue", {'hysteresis': temperature})

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOff(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["properties"]["switchOffValue"]["value"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOffMin(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOffValue"]["params"]["hysteresis"]["constraints"]["min"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOffMax(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOffValue"]["params"]["hysteresis"]["constraints"]["max"])

    @handleNotSupported
    def getDomesticHotWaterHysteresisSwitchOffStepping(self) -> float:
        return float(self.service.getProperty("heating.dhw.temperature.hysteresis")["commands"]["setHysteresisSwitchOffValue"]["params"]["hysteresis"]["constraints"]["stepping"])

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
        return self.service.setProperty("heating.dhw.temperature.hysteresis", "setHysteresisSwitchOffValue", {'hysteresis': temperature})


class Compressor(HeatingDeviceWithComponent):

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
    def getPhase(self):
        return self.service.getProperty(f"heating.compressors.{self.compressor}")["properties"]["phase"]["value"]
