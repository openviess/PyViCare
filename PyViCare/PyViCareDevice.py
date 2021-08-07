import logging
from datetime import datetime, time
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError, handleNotSupported

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

VICARE_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
VICARE_DHW_TEMP2 = "temp-2"


def isSupported(method):
    try:
        result = method()
        return result != 'error'
    except PyViCareNotSupportedFeatureError:
        return False


class Device:
    """This class connects to the Viesmann ViCare API.
    The authentication is done through OAuth2.
    Note that currently, a new token is generate for each run.
    """

    def __init__(self, service):
        self.service = service

    @property
    def circuits(self):
        return list([self.getCircuit(x) for x in self.getAvailableCircuits()])

    def getCircuit(self, circuit):
        return DeviceWithCircuit(self, circuit)

    @handleNotSupported
    def getOutsideTemperature(self):
        return self.service.getProperty("heating.sensors.temperature.outside")["properties"]["value"]["value"]

    @handleNotSupported
    def getDomesticHotWaterConfiguredTemperature(self):
        return self.service.getProperty("heating.dhw.temperature")["properties"]["value"]["value"]

    @handleNotSupported
    def getDomesticHotWaterConfiguredTemperature2(self):
        return self.service.getProperty("heating.dhw.temperature.temp2")["properties"]["value"]["value"]

    def getDomesticHotWaterActiveMode(self):
        schedule = self.getDomesticHotWaterSchedule()
        if schedule == "error" or schedule["active"] is not True:
            return None

        currentDateTime = datetime.now()
        currentTime = currentDateTime.time()

        current_day = VICARE_DAYS[currentDateTime.weekday()]
        if current_day not in schedule:
            return None

        mode = None
        for s in schedule[current_day]:
            startTime = time.fromisoformat(s["start"])
            endTime = time.fromisoformat(s["end"])
            if startTime <= currentTime and currentTime <= endTime:
                if s["mode"] == VICARE_DHW_TEMP2:  # temp-2 overrides all other modes
                    return s["mode"]
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
    def getDomesticHotWaterMaxTemperature(self):
        return self.service.getProperty("heating.dhw.temperature")["actions"][0]["fields"][0]["max"]

    @handleNotSupported
    def getDomesticHotWaterMinTemperature(self):
        return self.service.getProperty("heating.dhw.temperature")["actions"][0]["fields"][0]["min"]

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

    def setDomesticHotWaterTemperature(self, temperature):
        return self.service.setProperty("heating.dhw.temperature", "setTargetTemperature", {'temperature': temperature})

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

    def setDomesticHotWaterTemperature2(self, temperature):
        return self.service.setProperty("heating.dhw.temperature.temp2", "setTargetTemperature", {"temperature": temperature})

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
    def getSolarPumpActive(self):
        status = self.service.getProperty("heating.solar.pumps.circuit")[
            "properties"]["status"]["value"]
        return status == 'on'

    @handleNotSupported
    def getOneTimeCharge(self):
        return self.service.getProperty("heating.dhw.oneTimeCharge")["properties"]["active"]["value"]

    def deactivateOneTimeCharge(self):
        return self.service.setProperty("heating.dhw.oneTimeCharge", "deactivate", {})

    def activateOneTimeCharge(self):
        return self.service.setProperty("heating.dhw.oneTimeCharge", "activate", {})

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

        currentDateTime = datetime.now()
        currentTime = currentDateTime.time()

        current_day = VICARE_DAYS[currentDateTime.weekday()]
        if current_day not in schedule:
            return None  # no schedule for day configured

        for s in schedule[current_day]:
            startTime = time.fromisoformat(s["start"])
            endTime = time.fromisoformat(s["end"])
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


class DeviceWithCircuit:
    def __init__(self, device, circuit):
        self.service = device.service
        self.circuit = circuit
        self.device = device

    @property
    def id(self):
        return self.circuit

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
        return self.service.setProperty(f"heating.circuits.{self.circuit}.operating.programs.{program}", "setTemperature", {'targetTemperature': temperature})

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

    @handleNotSupported
    def getActiveProgram(self):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.operating.programs.active")["properties"]["value"]["value"]

    @handleNotSupported
    def getPrograms(self):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.operating.programs")["components"]

    @handleNotSupported
    def getDesiredTemperatureForProgram(self, program):
        return self.service.getProperty(f"heating.circuits.{self.circuit}.operating.programs.{program}")["properties"]["temperature"]["value"]

    @handleNotSupported
    def getCurrentDesiredTemperature(self):
        active_programm = self.getActiveProgram()
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
    def getTargetSupplyTemperature(self):
        if(not isSupported(self.getCurrentDesiredTemperature)
                or not isSupported(self.device.getOutsideTemperature)
                or not isSupported(self.getHeatingCurveShift)
                or not isSupported(self.getHeatingCurveSlope)):
            return None

        inside = self.getCurrentDesiredTemperature()
        outside = self.device.getOutsideTemperature()
        delta_outside_inside = (outside - inside)
        shift = self.getHeatingCurveShift()
        slope = self.getHeatingCurveSlope()
        targetSupply = (inside + shift - slope * delta_outside_inside
                        * (1.4347 + 0.021 * delta_outside_inside + 247.9
                            * pow(10, -6) * pow(delta_outside_inside, 2)))
        return round(targetSupply, 1)
