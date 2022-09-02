import logging
from contextlib import suppress
from typing import Any, Callable, List, Optional

from PyViCare.PyViCareHeatCurveCalculation import (
    heat_curve_formular_variant1, heat_curve_formular_variant2)
from PyViCare.PyViCareService import ViCareService
from PyViCare.PyViCareUtils import (PyViCareNotSupportedFeatureError,
                                    ViCareTimer, handleAPICommandErrors,
                                    handleNotSupported, parse_time_as_delta,
                                    time_as_delta)

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

VICARE_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
VICARE_DHW_TEMP2 = "temp-2"


def isSupported(method: Callable) -> bool:
    try:
        result = method()
        return bool(result != 'error')
    except PyViCareNotSupportedFeatureError:
        return False


def all_set(list: List[Any]) -> bool:
    return all(v is not None for v in list)


def get_available_burners(service):
    # workaround starting from 25.01.2022
    # see: https://github.com/somm15/PyViCare/issues/243
    available_burners = []
    for burner in ['0', '1', '2', '3', '4', '5']:
        with suppress(PyViCareNotSupportedFeatureError):
            if service.getProperty(f"heating.burners.{burner}") is not None:
                available_burners.append(burner)

    return available_burners


class Device:
    """This class connects to the Viesmann ViCare API.
    The authentication is done through OAuth2.
    Note that currently, a new token is generate for each run.
    """

    def __init__(self, service: ViCareService) -> None:
        self.service = service

    @property
    def circuits(self) -> List[Any]:
        return list([self.getCircuit(x) for x in self.getAvailableCircuits()])

    def getCircuit(self, circuit):
        return HeatingCircuit(self, circuit)

    def get_heat_curve_formular(self):
        if self.service.hasRoles(["type:heatpump", "type:E3"]):
            return heat_curve_formular_variant1
        if self.service.hasRoles(["type:heatpump"]) and len(self.getAvailableCircuits()) == 1:
            return heat_curve_formular_variant2
        return heat_curve_formular_variant1

    @property
    def burners(self) -> List[Any]:
        return []

    @property
    def compressors(self) -> List[Any]:
        return []

    @handleNotSupported
    def getOutsideTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.outside")["properties"]["value"]["value"]

    @handleNotSupported
    def getDomesticHotWaterConfiguredTemperature(self):
        return self.service.getProperty("heating.dhw.temperature.main")["properties"]["value"]["value"]

    @handleNotSupported
    def getHotWaterStorageTemperatureTop(self):
        return self.service.getProperty("heating.dhw.sensors.temperature.hotWaterStorage.top")["properties"]["value"]["value"]

    @handleNotSupported
    def getHotWaterStorageTemperatureBottom(self):
        return self.service.getProperty("heating.dhw.sensors.temperature.hotWaterStorage.bottom")["properties"]["value"]["value"]

    @handleNotSupported
    def getDomesticHotWaterConfiguredTemperature2(self):
        return self.service.getProperty("heating.dhw.temperature.temp2")["properties"]["value"]["value"]

    def getDomesticHotWaterActiveMode(self):
        schedule = self.getDomesticHotWaterSchedule()
        if schedule == "error" or schedule["active"] is not True:
            return None

        currentDateTime = ViCareTimer().now()
        currentTime = time_as_delta(currentDateTime)

        current_day = VICARE_DAYS[currentDateTime.weekday()]
        if current_day not in schedule:
            return None

        mode = None
        for s in schedule[current_day]:
            startTime = parse_time_as_delta(s["start"])
            endTime = parse_time_as_delta(s["end"])
            if startTime <= currentTime and currentTime <= endTime:
                if s["mode"] == VICARE_DHW_TEMP2:  # temp-2 overrides all other modes
                    return VICARE_DHW_TEMP2
                else:
                    mode = s["mode"]
        return mode

    def getDomesticHotWaterDesiredTemperature(self):
        mode = self.getDomesticHotWaterActiveMode()

        if mode is not None:
            if mode == VICARE_DHW_TEMP2:
                return self.getDomesticHotWaterConfiguredTemperature2()
            else:
                return self.getDomesticHotWaterConfiguredTemperature()

        return None

    @handleNotSupported
    def getDomesticHotWaterStorageTemperature(self):
        return self.service.getProperty("heating.dhw.sensors.temperature.hotWaterStorage")["properties"]["value"]["value"]

    @handleNotSupported
    def getDomesticHotWaterOutletTemperature(self):
        return self.service.getProperty("heating.dhw.sensors.temperature.outlet")["properties"]["value"]["value"]

    @handleNotSupported
    def getDomesticHotWaterPumpActive(self):
        status = self.service.getProperty("heating.dhw.pumps.primary")[
            "properties"]["status"]["value"]
        return status == 'on'

    @handleNotSupported
    def getDomesticHotWaterCirculationPumpActive(self):
        status = self.service.getProperty("heating.dhw.pumps.circulation")[
            "properties"]["status"]["value"]
        return status == 'on'

    @handleNotSupported
    def getDomesticHotWaterActive(self):
        status = self.service.getProperty("heating.dhw")["properties"]["status"]["value"]
        return status == 'on'

    @handleNotSupported
    def getDomesticHotWaterMaxTemperature(self):
        return self.service.getProperty("heating.dhw.temperature.main")["commands"]["setTargetTemperature"]["params"]["temperature"]["constraints"]["max"]

    @handleNotSupported
    def getDomesticHotWaterMinTemperature(self):
        return self.service.getProperty("heating.dhw.temperature.main")["commands"]["setTargetTemperature"]["params"]["temperature"]["constraints"]["min"]

    @handleNotSupported
    def getDomesticHotWaterChargingActive(self):
        return self.service.getProperty("heating.dhw.charging")["properties"]["active"]["value"]

    """ Set the target temperature for domestic host water
    Parameters
    ----------
    temperature : int
        Target temperature

    Returns
    -------
    result: json
        json representation of the answer
    """

    @handleAPICommandErrors
    def setDomesticHotWaterTemperature(self, temperature):
        return self.service.setProperty("heating.dhw.temperature.main", "setTargetTemperature", {'temperature': int(temperature)})

    """ Set the target temperature 2 for domestic host water
    Parameters
    ----------
    temperature : int
        Target temperature

    Returns
    -------
    result: json
        json representation of the answer
    """

    @handleAPICommandErrors
    def setDomesticHotWaterTemperature2(self, temperature):
        return self.service.setProperty("heating.dhw.temperature.temp2", "setTargetTemperature", {"temperature": int(temperature)})

    @handleNotSupported
    def getDomesticHotWaterSchedule(self):
        properties = self.service.getProperty(
            "heating.dhw.schedule")["properties"]
        return {
            "active": properties["active"]["value"],
            "mon": properties["entries"]["value"]["mon"],
            "tue": properties["entries"]["value"]["tue"],
            "wed": properties["entries"]["value"]["wed"],
            "thu": properties["entries"]["value"]["thu"],
            "fri": properties["entries"]["value"]["fri"],
            "sat": properties["entries"]["value"]["sat"],
            "sun": properties["entries"]["value"]["sun"]
        }

    @handleNotSupported
    def getSolarCollectorTemperature(self):
        return self.service.getProperty("heating.solar.sensors.temperature.collector")["properties"]["value"]["value"]

    @handleNotSupported
    def getSolarStorageTemperature(self):
        return self.service.getProperty("heating.solar.sensors.temperature.dhw")["properties"]["value"]["value"]

    @handleNotSupported
    def getSolarPowerProduction(self):
        return self.getSolarPowerProductionDays()

    @handleNotSupported
    def getSolarPowerProductionUnit(self):
        return self.service.getProperty("heating.solar.power.production")["properties"]["day"]["unit"]

    @handleNotSupported
    def getSolarPowerProductionDays(self):
        return self.service.getProperty("heating.solar.power.production")["properties"]["day"]["value"]

    @handleNotSupported
    def getSolarPowerProductionToday(self):
        return self.service.getProperty("heating.solar.power.production")["properties"]["day"]["value"][0]

    @handleNotSupported
    def getSolarPowerProductionWeeks(self):
        return self.service.getProperty("heating.solar.power.production")["properties"]["week"]["value"]

    @handleNotSupported
    def getSolarPowerProductionThisWeek(self):
        return self.service.getProperty("heating.solar.power.production")["properties"]["week"]["value"][0]

    @handleNotSupported
    def getSolarPowerProductionMonths(self):
        return self.service.getProperty("heating.solar.power.production")["properties"]["month"]["value"]

    @handleNotSupported
    def getSolarPowerProductionThisMonth(self):
        return self.service.getProperty("heating.solar.power.production")["properties"]["month"]["value"][0]

    @handleNotSupported
    def getSolarPowerProductionYears(self):
        return self.service.getProperty("heating.solar.power.production")["properties"]["year"]["value"]

    @handleNotSupported
    def getSolarPowerProductionThisYear(self):
        return self.service.getProperty("heating.solar.power.production")["properties"]["year"]["value"][0]

    @handleNotSupported
    def getSolarPumpActive(self):
        status = self.service.getProperty("heating.solar.pumps.circuit")[
            "properties"]["status"]["value"]
        return status == 'on'

    @handleNotSupported
    def getOneTimeCharge(self):
        return self.service.getProperty("heating.dhw.oneTimeCharge")["properties"]["active"]["value"]

    @handleAPICommandErrors
    def deactivateOneTimeCharge(self):
        return self.service.setProperty("heating.dhw.oneTimeCharge", "deactivate", {})

    @handleAPICommandErrors
    def activateOneTimeCharge(self):
        return self.service.setProperty("heating.dhw.oneTimeCharge", "activate", {})

    @handleAPICommandErrors
    def setDomesticHotWaterCirculationSchedule(self, schedule):
        return self.service.setProperty("heating.dhw.pumps.circulation.schedule", "setSchedule", {'newSchedule': schedule})

    @handleNotSupported
    def getDomesticHotWaterCirculationScheduleModes(self):
        return self.service.getProperty("heating.dhw.pumps.circulation.schedule")["commands"]["setSchedule"]["params"]["newSchedule"]["constraints"]["modes"]

    @handleNotSupported
    def getDomesticHotWaterCirculationSchedule(self):
        schedule = self.service.getProperty(
            "heating.dhw.pumps.circulation.schedule")

        properties = schedule["properties"]
        command = schedule["commands"]
        return {
            "active": properties["active"]["value"],
            "default_mode": command["setSchedule"]["params"]["newSchedule"]["constraints"]["defaultMode"],
            "mon": properties["entries"]["value"]["mon"],
            "tue": properties["entries"]["value"]["tue"],
            "wed": properties["entries"]["value"]["wed"],
            "thu": properties["entries"]["value"]["thu"],
            "fri": properties["entries"]["value"]["fri"],
            "sat": properties["entries"]["value"]["sat"],
            "sun": properties["entries"]["value"]["sun"]
        }

    def getDomesticHotWaterCirculationMode(self):
        schedule = self.getDomesticHotWaterCirculationSchedule()
        if schedule == "error" or schedule["active"] is not True:
            return None

        currentDateTime = ViCareTimer().now()
        currentTime = time_as_delta(currentDateTime)

        current_day = VICARE_DAYS[currentDateTime.weekday()]
        if current_day not in schedule:
            return None  # no schedule for day configured

        for s in schedule[current_day]:
            startTime = parse_time_as_delta(s["start"])
            endTime = parse_time_as_delta(s["end"])
            if startTime <= currentTime and currentTime <= endTime:
                return s["mode"]
        return schedule['default_mode']

    @handleNotSupported
    def getAvailableCircuits(self):
        return self.service.getProperty("heating.circuits")["properties"]["enabled"]["value"]

    @handleNotSupported
    def getControllerSerial(self):
        return self.service.getProperty("heating.controller.serial")["properties"]["value"]["value"]

    @handleNotSupported
    def getBoilerSerial(self):
        return self.service.getProperty("heating.boiler.serial")["properties"]["value"]["value"]

    @handleNotSupported
    def getSerial(self):
        return self.service.getProperty("device.serial")["properties"]["value"]["value"]

    @handleNotSupported
    def getReturnTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.return")["properties"]["value"]["value"]

    @handleNotSupported
    def getSupplyTemperaturePrimaryCircuit(self):
        return self.service.getProperty("heating.primaryCircuit.sensors.temperature.supply")["properties"]["value"]["value"]

    @handleNotSupported
    def getReturnTemperaturePrimaryCircuit(self):
        return self.service.getProperty("heating.primaryCircuit.sensors.temperature.return")["properties"]["value"]["value"]

    @handleNotSupported
    def getSupplyTemperatureSecondaryCircuit(self):
        return self.service.getProperty("heating.secondaryCircuit.sensors.temperature.supply")["properties"]["value"]["value"]

    @handleNotSupported
    def getReturnTemperatureSecondaryCircuit(self):
        return self.service.getProperty("heating.secondaryCircuit.sensors.temperature.return")["properties"]["value"]["value"]


class DeviceWithComponent:
    def __init__(self, device: Device, component: str) -> None:
        self.service = device.service
        self.component = component
        self.device = device

    @property
    def id(self) -> str:
        return self.component


class HeatingCircuit(DeviceWithComponent):

    @property
    def circuit(self) -> str:
        return self.component

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

    def setMode(self, mode):
        r = self.service.setProperty(
            f"heating.circuits.{self.circuit}.operating.modes.active", "setMode", {'mode': mode})
        return r

    # Works for normal, reduced, comfort
    # active has no action
    # external, standby no action
    # holiday, scheduled and unscheduled
    # activate, decativate comfort, eco
    """ Set the target temperature for the target program
    Parameters
    ----------
    program : str
        Can be normal, reduced or comfort
    temperature: int
        target temperature

    Returns
    -------
    result: json
        json representation of the answer
    """

    def setProgramTemperature(self, program: str, temperature: int):
        return self.service.setProperty(f"heating.circuits.{self.circuit}.operating.programs.{program}", "setTemperature", {'targetTemperature': int(temperature)})

    def setReducedTemperature(self, temperature):
        return self.setProgramTemperature("reduced", temperature)

    def setComfortTemperature(self, temperature):
        return self.setProgramTemperature("comfort", temperature)

    def setNormalTemperature(self, temperature):
        return self.setProgramTemperature("normal", temperature)

    """ Activate a program
        NOTE
        DEVICE_COMMUNICATION_ERROR can just mean that the program is already on
    Parameters
    ----------
    program : str
        Appears to work only for comfort

    Returns
    -------
    result: json
        json representation of the answer
    """
    # optional temperature parameter could be passed (but not done)

    def activateProgram(self, program):
        return self.service.setProperty(f"heating.circuits.{self.circuit}.operating.programs.{program}", "activate", {})

    def activateComfort(self):
        return self.activateProgram("comfort")

    """ Deactivate a program
    Parameters
    ----------
    program : str
        Appears to work only for comfort and eco (coming from normal, can be reached only by deactivating another state)

    Returns
    -------
    result: json
        json representation of the answer
    """

    def deactivateProgram(self, program):
        return self.service.setProperty(f"heating.circuits.{self.circuit}.operating.programs.{program}", "deactivate", {})

    def deactivateComfort(self):
        return self.deactivateProgram("comfort")

    @handleNotSupported
    def getSupplyTemperature(self):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.sensors.temperature.supply")["properties"]["value"]["value"]

    @handleNotSupported
    def getRoomTemperature(self):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.sensors.temperature.room")["properties"]["value"]["value"]

    @handleNotSupported
    def getModes(self):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.operating.modes.active")["commands"]["setMode"]["params"]["mode"]["constraints"]["enum"]

    @handleNotSupported
    def getActiveMode(self):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.operating.modes.active")["properties"]["value"]["value"]

    @handleNotSupported
    def getHeatingCurveShift(self):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.heating.curve")["properties"]["shift"]["value"]

    @handleNotSupported
    def getHeatingCurveSlope(self):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.heating.curve")["properties"]["slope"]["value"]

    @handleAPICommandErrors
    def setHeatingCurve(self, shift, slope):
        return self.service.setProperty(f"heating.circuits.{self.circuit}.heating.curve", "setCurve", {'shift': int(shift), 'slope': round(float(slope), 1)})

    @handleNotSupported
    def getActiveProgram(self):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.operating.programs.active")["properties"]["value"]["value"]

    @handleNotSupported
    def getPrograms(self):
        available_programs = []
        for program in ['active', 'comfort', 'forcedLastFromSchedule', 'eco', 'external', 'fixed', 'holiday', 'normal', 'reduced', 'standby']:
            with suppress(PyViCareNotSupportedFeatureError):
                if self.service.getProperty(f"heating.circuits.{self.circuit}.operating.programs.{program}") is not None:
                    available_programs.append(program)

        return available_programs

    @handleNotSupported
    def getDesiredTemperatureForProgram(self, program):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.operating.programs.{program}")["properties"]["temperature"]["value"]

    @handleNotSupported
    def getCurrentDesiredTemperature(self):
        active_programm = self.getActiveProgram()
        if active_programm in ['standby']:
            return None
        return self.service.getProperty(f"heating.circuits.{self.circuit}.operating.programs.{active_programm}")["properties"]["temperature"]["value"]

    @handleNotSupported
    def getFrostProtectionActive(self):
        status = self.service.getProperty(f"heating.circuits.{self.circuit}.frostprotection")[
            "properties"]["status"]["value"]
        return status == 'on'

    @handleNotSupported
    def getCirculationPumpActive(self):
        status = self.service.getProperty(f"heating.circuits.{self.circuit}.circulation.pump")[
            "properties"]["status"]["value"]
        return status == 'on'

    @handleNotSupported
    def getTemperatureLevelsMin(self):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.temperature.levels")["properties"]["min"]["value"]

    @handleNotSupported
    def getTemperatureLevelsMax(self):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.temperature.levels")["properties"]["max"]["value"]

    @handleNotSupported
    def getHeatingSchedule(self):
        properties = self.service.getProperty(
            f"heating.circuits.{self.circuit}.heating.schedule")["properties"]
        return {
            "active": properties["active"]["value"],
            "mon": properties["entries"]["value"]["mon"],
            "tue": properties["entries"]["value"]["tue"],
            "wed": properties["entries"]["value"]["wed"],
            "thu": properties["entries"]["value"]["thu"],
            "fri": properties["entries"]["value"]["fri"],
            "sat": properties["entries"]["value"]["sat"],
            "sun": properties["entries"]["value"]["sun"]
        }

    # Calculates target supply temperature based on data from Viessmann
    # See: https://www.viessmann-community.com/t5/Gas/Mathematische-Formel-fuer-Vorlauftemperatur-aus-den-vier/m-p/68890#M27556
    def getTargetSupplyTemperature(self) -> Optional[float]:
        inside = None
        outside = None
        shift = None
        slope = None
        with suppress(PyViCareNotSupportedFeatureError):
            inside = self.getCurrentDesiredTemperature()
            outside = self.device.getOutsideTemperature()
            shift = self.getHeatingCurveShift()
            slope = self.getHeatingCurveSlope()

        if(not all_set([inside, outside, shift, slope])):
            return None

        max_value = None
        min_value = None
        with suppress(PyViCareNotSupportedFeatureError):
            max_value = self.getTemperatureLevelsMax()
            min_value = self.getTemperatureLevelsMin()

        delta_outside_inside = (outside - inside)
        target_supply = self.device.get_heat_curve_formular()(delta_outside_inside, inside, shift, slope)

        if all_set([min_value, max_value]):
            target_supply = max(min_value, min(target_supply, max_value))

        return float(round(target_supply, 1))
