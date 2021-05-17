#!/usr/bin/python3
 
from re import I
import sys
import json
import logging
sys.path.insert(0, '/Users/pfeifera/VS.code/PyViCare')
from PyViCare.PyViCareGazBoiler import GazBoiler

from datetime import datetime

now = datetime.now()

current_time = now.strftime("%d.%m.%Y %H:%M:%S")
epoch = now.strftime("%s")

t=GazBoiler("user@mail.de","passwordhere","token.save")


print("----", current_time, "---------------------------------------------------------------------------")

# get all in one request
result = t.getAllEntries()
# count all entities
entity_count = len(result['entities'])

# heating circuit is allways 0
# handle every entry individually

# start
# ("heating.circuits.0.operating.programs.active")["properties"]["value"]["value"
HeatingProgram = ''
# beware of longer matches
device_feature = '\'heating.circuits.0.operating.programs.active\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingProgram = str(result['entities'][feature_number]['properties']['value']['value'])
        break
print (device_feature, HeatingProgram)
# end

# start
# ("heating.sensors.temperature.outside")["properties"]["value"]["value"]
HeatingOutsideTemperature = 0
# beware of longer matches
device_feature = '\'heating.sensors.temperature.outside\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingOutsideTemperature = str(result['entities'][feature_number]['properties']['value']['value'])
        break
print (device_feature, HeatingOutsideTemperature)
# end

# start
# ("heating.circuits.0.operating.programs.HeatingProgram")["properties"]["temperature"]["value"]
DesiredTemperature = 3
# beware of longer matches
# fallback value for desired temp
device_feature = '\'heating.circuits.0.operating.programs.'+HeatingProgram+'\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        DesiredTemperature = str(result['entities'][feature_number]['properties']['temperature']['value'])
        break
print (device_feature, "DesiredTemperature", DesiredTemperature)
# end

# start
# ("heating.circuits.0.heating.curve")["properties"]["shift"]["value"
Shift = 0
# ("heating.circuits.0.heating.curve")["properties"]["slope"]["value"
Slope = 1
# beware of longer matches
device_feature = '\'heating.circuits.0.heating.curve\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        Shift = str(result['entities'][feature_number]['properties']['shift']['value'])
        Slope = str(result['entities'][feature_number]['properties']['slope']['value'])
        break
print (device_feature, "Shift", Shift)
print (device_feature, "Slope", Slope)
# end

# Calculates target supply temperature based on data from Viessmann
# See: https://www.viessmann-community.com/t5/Gas/Mathematische-Formel-fuer-Vorlauftemperatur-aus-den-vier/m-p/68890#M27556
delta_outside_inside = float(HeatingOutsideTemperature) - float(DesiredTemperature)
HeatingSupplyTemperatureTarget = round((float(DesiredTemperature) + float(Shift) - float(Slope) * delta_outside_inside * (1.4347 + 0.021 * delta_outside_inside + 247.9 * pow(10, -6) * pow(delta_outside_inside, 2))),1)
# less than 20 makes no sense, fallback to minimal 20 supply temp
if HeatingSupplyTemperatureTarget < 20 :
    HeatingSupplyTemperatureTarget = 20

print ("'HeatingSupplyTemperatureTarget'", HeatingSupplyTemperatureTarget)

# start
# ("heating.circuits.0.sensors.temperature.supply")["properties"]["value"]["value"
HeatingSupplyTemperature = 20
# beware of longer matches
device_feature = '\'heating.circuits.0.sensors.temperature.supply\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingSupplyTemperature = str(result['entities'][feature_number]['properties']['value']['value'])
        break
print (device_feature, HeatingSupplyTemperature)
# end

# start
# ("heating.dhw.temperature")["properties"]["value"]["value"]
# the normal temperature here
HeatingDHWTemperatureTarget = 60
# beware of longer matches
device_feature = '\'heating.dhw.temperature\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingDHWTemperatureTarget = str(result['entities'][feature_number]['properties']['value']['value'])
        break
#print (device_feature, HeatingDHWTemperatureTarget)
# end

# start
# ("heating.dhw.temperature.temp2")["properties"]["value"]["value"]
# hygiene temp2, if exists will overwrite the temp from before
# HeatingDHWTemperatureTarget2
# beware of longer matches
device_feature = '\'heating.dhw.temperature.temp2\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingDHWTemperatureTarget = str(result['entities'][feature_number]['properties']['value']['value'])
        break
#print (device_feature, HeatingDHWTemperatureTarget)
# end
#print only the last read temp for dhw

print ("'HeatingDHWTemperatureTarget'", HeatingDHWTemperatureTarget)

# start
# ("heating.dhw.sensors.temperature.hotWaterStorage")["properties"]["value"]["value"]
HeatingDHWTemperature = 20
# beware of longer matches
device_feature = '\'heating.dhw.sensors.temperature.hotWaterStorage\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingDHWTemperature = str(result['entities'][feature_number]['properties']['value']['value'])
        break
print (device_feature, HeatingDHWTemperature)
# end

# start
# ("heating.valves.diverter.heatDhw")["properties"]["position"]["value"]
HeatingMode = ''
# beware of longer matches
device_feature = '\'heating.valves.diverter.heatDhw\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingMode = str(result['entities'][feature_number]['properties']['position']['value'])
        break
print (device_feature, HeatingMode)
# end

# start
# ("heating.burner")["properties"]["active"]["value"
HeatingBurnerStatus = ''
# beware of longer matches
device_feature = '\'heating.burner\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingBurnerStatus = str(result['entities'][feature_number]['properties']['active']['value'])
        break
print (device_feature, HeatingBurnerStatus)
# end

# start
# ('heating.burner.modulation')["properties"]["value"]["value"
HeatingBurnerModulation = 0
# beware of longer matches
device_feature = '\'heating.burner.modulation\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingBurnerModulation = str(result['entities'][feature_number]['properties']['value']['value'])
        break
print (device_feature, HeatingBurnerModulation)
# end

# start
# ("heating.circuits.0.circulation.pump")["properties"]["status"]["value"
HeatingCirculationPump = ''
# beware of longer matches
device_feature = '\'heating.circuits.0.circulation.pump\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingCirculationPump = str(result['entities'][feature_number]['properties']['status']['value'])
        break
print (device_feature, HeatingCirculationPump )
# end

# start
# ("heating.dhw.pumps.primary")["properties"]["status"]["value"]
HeatingDHWCirculationPump = ''
# beware of longer matches
device_feature = '\'heating.dhw.pumps.primary\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingDHWCirculationPump = str(result['entities'][feature_number]['properties']['status']['value'])
        break
print (device_feature, HeatingDHWCirculationPump )
# end

# start
# ('heating.gas.consumption.heating')['properties']['day']['value'][0]
HeatingGasConsumptionHeating = 0
# beware of longer matches
device_feature = '\'heating.gas.consumption.heating\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingGasConsumptionHeating = str(result['entities'][feature_number]['properties']['day']['value'][0])
        break
print (device_feature, HeatingGasConsumptionHeating )
# end

# start
# ('heating.gas.consumption.dhw')['properties']['day']['value'][0]
HeatingGasConsumptionDHW = 0
# beware of longer matches
device_feature = '\'heating.gas.consumption.dhw\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingGasConsumptionDHW = str(result['entities'][feature_number]['properties']['day']['value'][0])
        break
print (device_feature, HeatingGasConsumptionDHW )
# end

# start
# 'heating.power.consumption.total')['properties']['day']['value'][0]
HeatingPowerConsumption = 0
# beware of longer matches
device_feature = '\'heating.power.consumption.total\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingPowerConsumption = str(result['entities'][feature_number]['properties']['day']['value'][0])
        break
print (device_feature, HeatingPowerConsumption )
# end

# start
# ('heating.burner.statistics')['properties']['hours']['value'
HeatingBurnerHours = 0
# ('heating.burner.statistics')['properties']['starts']['value'
HeatingBurnerStarts = 0
# beware of longer matches
device_feature = '\'heating.burner.statistics\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingBurnerHours = str(result['entities'][feature_number]['properties']['hours']['value'])
        HeatingBurnerStarts = str(result['entities'][feature_number]['properties']['starts']['value'])
        break
print (device_feature, "hours", HeatingBurnerHours )
print (device_feature, "starts", HeatingBurnerStarts )
# end

# start
# ('heating.sensors.pressure.supply')['properties']['value']['value']
HeatingSupplyPressure = 0
# beware of longer matches
device_feature = '\'heating.sensors.pressure.supply\''
for feature_number in range(entity_count) :
    feature = str(result['entities'][feature_number]['class'])
    #print (feature_number, feature)
    if device_feature in feature :
        HeatingSupplyPressure = str(result['entities'][feature_number]['properties']['value']['value'])
        break
print (device_feature, HeatingSupplyPressure )
# end


print("----------------------------------------------------------------------------------------------------")
