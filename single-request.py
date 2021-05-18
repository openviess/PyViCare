#!/usr/bin/python3
 
from re import I
import sys
import json
import logging
from datetime import datetime

#sys.path.insert(0, 'PyViCare')
from PyViCare.PyViCareGazBoiler import GazBoiler



logger = logging.getLogger('single-request')
logger.setLevel(logging.DEBUG)

# logger.addHandler(logging.NullHandler())
# logger.addHandler(logging.FileHandler('pyvicare.log', mode='a'))
logger.addHandler(logging.StreamHandler())
now = datetime.now()

current_time = now.strftime("%d.%m.%Y %H:%M:%S")
epoch = now.strftime("%s")

t=GazBoiler("user@mail.io","passowrd-here","token.save")


logger.debug ("----"+str(current_time)+"---------------------------------------------------------------------------")

# get all in one request
result = t.getAllEntries()
# count all entities
entity_count = len(result['entities'])

# heating circuit is allways 0
# handle every entry individually
# beware of longer matches

HeatingProgram = 'standby'
HeatingOutsideTemperature = 0
DesiredTemperature = 3
Shift = 0
Slope = 1
HeatingSupplyTemperature = 20
HeatingDHWTemperatureTarget = 60
HeatingDHWTemperature = 20
# heating or heatingDhw
HeatingMode = 'heating'
HeatingBurnerStatus = 'False'
HeatingBurnerModulation = 0
HeatingCirculationPump = 'off'
HeatingDHWCirculationPump = 'fake'
HeatingGasConsumptionHeating = 0
HeatingGasConsumptionDHW = 0
HeatingPowerConsumption = 0
HeatingBurnerHours = 0
HeatingBurnerStarts = 0
HeatingSupplyPressure = 0

# extra run to get HeatingProgram
# ("heating.circuits.0.operating.programs.active")["properties"]["value"]["value"
device_feature = '\'heating.circuits.0.operating.programs.active\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    if device_feature in feature :
        HeatingProgram = str(result['entities'][feature_number]['properties']['value']['value'])
        break
logger.debug (device_feature + ' : ' + HeatingProgram)

for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    
    # ("heating.sensors.temperature.outside")["properties"]["value"]["value"]
    device_feature = '\'heating.sensors.temperature.outside\''
    if device_feature in feature :
        HeatingOutsideTemperature = str(result['entities'][feature_number]['properties']['value']['value'])
        logger.debug (device_feature + ' : ' + str(HeatingOutsideTemperature))

    # ("heating.circuits.0.operating.programs.HeatingProgram")["properties"]["temperature"]["value"]
    # fallback value for desired temp
    device_feature = '\'heating.circuits.0.operating.programs.'+HeatingProgram+'\''
    if device_feature in feature :
        try :
            DesiredTemperature = str(result['entities'][feature_number]['properties']['temperature']['value'])
        except :
            DesiredTemperature = 3
        logger.debug (device_feature + ' : ' + "DesiredTemperature" + ' : ' + str(DesiredTemperature))
    # ("heating.circuits.0.heating.curve")["properties"]["shift"]["value"
    # ("heating.circuits.0.heating.curve")["properties"]["slope"]["value"
    device_feature = '\'heating.circuits.0.heating.curve\''
    if device_feature in feature :
        Shift = str(result['entities'][feature_number]['properties']['shift']['value'])
        Slope = str(result['entities'][feature_number]['properties']['slope']['value'])
        logger.debug (device_feature + ' : ' + "Shift" + ' : ' + str(Shift))
        logger.debug (device_feature + ' : ' + "Slope" + ' : ' + str(Slope))

    # Calculates target supply temperature based on data from Viessmann
    # See: https://www.viessmann-community.com/t5/Gas/Mathematische-Formel-fuer-Vorlauftemperatur-aus-den-vier/m-p/68890#M27556
    delta_outside_inside = float(HeatingOutsideTemperature) - float(DesiredTemperature)
    HeatingSupplyTemperatureTarget = round((float(DesiredTemperature) + float(Shift) - float(Slope) * delta_outside_inside * (1.4347 + 0.021 * delta_outside_inside + 247.9 * pow(10, -6) * pow(delta_outside_inside, 2))),1)
    # less than 20 makes no sense, fallback to minimal 20 supply temp
    if HeatingSupplyTemperatureTarget < 20 :
        HeatingSupplyTemperatureTarget = 20

    # ("heating.circuits.0.sensors.temperature.supply")["properties"]["value"]["value"
    device_feature = '\'heating.circuits.0.sensors.temperature.supply\''
    if device_feature in feature :
        HeatingSupplyTemperature = str(result['entities'][feature_number]['properties']['value']['value'])
        logger.debug (device_feature + ' : ' + str(HeatingSupplyTemperature))
        logger.debug ('\'HeatingSupplyTemperatureTarget\'' + ' : ' + str(HeatingSupplyTemperatureTarget))

    # ("heating.dhw.temperature")["properties"]["value"]["value"]
    # the normal temperature here
    device_feature = '\'heating.dhw.temperature\''
    if device_feature in feature :
        HeatingDHWTemperatureTarget = str(result['entities'][feature_number]['properties']['value']['value'])
        logger.debug ("'HeatingDHWTemperatureTarget'" + ' : ' + HeatingDHWTemperatureTarget)

    # ("heating.dhw.temperature.temp2")["properties"]["value"]["value"]
    # hygiene temp2, if exists will overwrite the temp from before
    # HeatingDHWTemperatureTarget2
    device_feature = '\'heating.dhw.temperature.temp2\''
    if device_feature in feature :
        HeatingDHWTemperatureTarget = str(result['entities'][feature_number]['properties']['value']['value'])
        logger.debug ("'HeatingDHWTemperatureTarget'" + ' : ' + HeatingDHWTemperatureTarget)

    # ("heating.dhw.sensors.temperature.hotWaterStorage")["properties"]["value"]["value"]
    device_feature = '\'heating.dhw.sensors.temperature.hotWaterStorage\''
    if device_feature in feature :
        HeatingDHWTemperature = str(result['entities'][feature_number]['properties']['value']['value'])
        logger.debug (device_feature + ' : ' + HeatingDHWTemperature)

    # ("heating.valves.diverter.heatDhw")["properties"]["position"]["value"]
    device_feature = '\'heating.valves.diverter.heatDhw\''
    if device_feature in feature :
        HeatingMode = str(result['entities'][feature_number]['properties']['position']['value'])
        logger.debug (device_feature + ' : ' + HeatingMode)

    # ("heating.burner")["properties"]["active"]["value"
    device_feature = '\'heating.burner\''
    if device_feature in feature :
        HeatingBurnerStatus = str(result['entities'][feature_number]['properties']['active']['value'])
        logger.debug (device_feature + ' : ' + HeatingBurnerStatus)

    # ('heating.burner.modulation')["properties"]["value"]["value"
    device_feature = '\'heating.burner.modulation\''
    if device_feature in feature :
        HeatingBurnerModulation = str(result['entities'][feature_number]['properties']['value']['value'])
        logger.debug (device_feature + ' : ' + HeatingBurnerModulation)

    # ("heating.circuits.0.circulation.pump")["properties"]["status"]["value"
    device_feature = '\'heating.circuits.0.circulation.pump\''
    if device_feature in feature :
        HeatingCirculationPump = str(result['entities'][feature_number]['properties']['status']['value'])
        logger.debug (device_feature + ' : ' + HeatingCirculationPump )

    # ("heating.dhw.pumps.primary")["properties"]["status"]["value"]
    device_feature = '\'heating.dhw.pumps.circulation\''
    if device_feature in feature :
        HeatingDHWCirculationPump = str(result['entities'][feature_number]['properties']['status']['value'])
        logger.debug (device_feature + ' : ' + HeatingDHWCirculationPump )

    # ('heating.gas.consumption.heating')['properties']['day']['value'][0]
    device_feature = '\'heating.gas.consumption.heating\''
    if device_feature in feature :
        HeatingGasConsumptionHeating = str(result['entities'][feature_number]['properties']['day']['value'][0])
        logger.debug (device_feature + ' : ' + HeatingGasConsumptionHeating )

    # ('heating.gas.consumption.dhw')['properties']['day']['value'][0]
    device_feature = '\'heating.gas.consumption.dhw\''
    if device_feature in feature :
        HeatingGasConsumptionDHW = str(result['entities'][feature_number]['properties']['day']['value'][0])
        logger.debug (device_feature + ' : ' + HeatingGasConsumptionDHW )

    # 'heating.power.consumption.total')['properties']['day']['value'][0]
    device_feature = '\'heating.power.consumption.total\''
    if device_feature in feature :
        HeatingPowerConsumption = str(result['entities'][feature_number]['properties']['day']['value'][0])
        logger.debug (device_feature + ' : ' + HeatingPowerConsumption )

    # ('heating.burner.statistics')['properties']['hours']['value'
    # ('heating.burner.statistics')['properties']['starts']['value'
    device_feature = '\'heating.burner.statistics\''
    if device_feature in feature :
        HeatingBurnerHours = str(result['entities'][feature_number]['properties']['hours']['value'])
        HeatingBurnerStarts = str(result['entities'][feature_number]['properties']['starts']['value'])
        logger.debug (device_feature + ' : ' + "hours" + ' : ' + HeatingBurnerHours )
        logger.debug (device_feature + ' : ' + "starts" + ' : ' + HeatingBurnerStarts )

    # ('heating.sensors.pressure.supply')['properties']['value']['value']
    device_feature = '\'heating.sensors.pressure.supply\''
    if device_feature in feature :
        HeatingSupplyPressure = str(result['entities'][feature_number]['properties']['value']['value'])
        logger.debug (device_feature + ' : ' + HeatingSupplyPressure )


logger.debug ("----------------------------------------------------------------------------------------------------")



print("epoch=", epoch, sep='', end=',')
print("HeatingOutsideTemperature=", HeatingOutsideTemperature, sep='', end=',')
print("HeatingSupplyTemperatureTarget=", HeatingSupplyTemperatureTarget, sep='', end=',')
print("HeatingSupplyTemperature=", HeatingSupplyTemperature, sep='', end=',')
print("HeatingDHWTemperatureTarget=", HeatingDHWTemperatureTarget, sep='', end=',')
print("HeatingDHWTemperature=", HeatingDHWTemperature, sep='', end=',')
print("HeatingProgram=", HeatingProgram, sep='', end=',')
print("HeatingMode=", HeatingMode, sep='', end=',')
print("HeatingBurnerStatus=", HeatingBurnerStatus, sep='', end=',')
print("HeatingBurnerModulation=", HeatingBurnerModulation, sep='', end=',')
print("HeatingCirculationPump=", HeatingCirculationPump, sep='', end=',')
print("HeatingDHWCirculationPump=", HeatingDHWCirculationPump, sep='', end=',')
print("HeatingGasConsumptionHeating=", HeatingGasConsumptionHeating, sep='', end=',') 
print("HeatingGasConsumptionDHW=", HeatingGasConsumptionDHW, sep='', end=',')
print("HeatingPowerConsumption=", HeatingGasConsumptionDHW, sep='', end=',')
print("HeatingBurnerHours=", HeatingBurnerHours, sep='', end=',')
print("HeatingBurnerStarts=", HeatingBurnerStarts, sep='', end=',')
print("HeatingSupplyPressure=", HeatingSupplyPressure, sep='')