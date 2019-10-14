# PyViCare

Implements an object to interact with the Viessmann ViCare API.
The OAuth2 authentication token can optionally be stored in a file to be reused.
Tokens are automatically renewed.

A few nice feature removed from the app are available though the API (Comfort and Eco modes).

## Version 0.1.0
Note that the version 0.1.0 DOES BREAK a few things.
ViCareSession is deprecated (but you can still import it using f"rom PyViCare.PyViCare import ViCareSession").
You can now use the following objects:
```
from PyViCare.PyViCareDevice import Device # generic device
from PyViCare.PyViCareGazBoiler import GazBoiler # gaz boiler
from PyViCare.PyViCareHeatPump import HeatPump # heat pump
```

## Basic usage
Simple example:
```
import sys
import logging
sys.path.insert(0, 'PyViCare')
from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareService import ViCareService
from PyViCare.PyViCare import ViCareSession

t=GazBoiler("email@domain","password","token.save")
print(t.getDomesticHotWaterConfiguredTemperature()) 
print(t.getDomesticHotWaterStorageTemperature())
print(t.getOutsideTemperature())
print(t.getRoomTemperature())
print(t.getSupplyTemperature())
print(t.getOutsideTemperature()) 
print(t.getHeatingCurveShift()) 
print(t.getHeatingCurveSlope()) 
print(t.getBoilerTemperature())
print(t.getActiveProgram())
print(t.getPrograms())

print(t.getCurrentDesiredTemperature())
print(t.getMonthSinceLastService())
print(t.getLastServiceDate())

print(t.getDesiredTemperatureForProgram("comfort"))
print(t.getActiveMode())

print(t.getDesiredTemperatureForProgram("comfort"))
print(t.setProgramTemperature("comfort",21))
print(t.activateProgram("comfort"))
print(t.setDomesticHotWaterTemperature(59))
print(t.activateProgram("comfort"))
print(t.deactivateComfort())
```

## Postman example

Follow these steps to access the API in Postman:

1. Create an access token in the `Authorization` tab with type `OAuth 2.0` and following inputs:

    - Client id: 79742319e39245de5f91d15ff4cac2a8
    - Secret id: 8ad97aceb92c5892e102b093c7c083fa
    - Callback url: vicare://oauth-callback/everest
    - Auth url: https://iam.viessmann.com/idp/v1/authorize
    - Access token url: https://iam.viessmann.com/idp/v1/token
    - Scope: openid

    A login popup will open. Enter your ViCare username and password.

2. Use this URL to access your `installationId` and `gatewaySerial`: 

    `https://api.viessmann-platform.io/general-management/installations`

    - `installationId` is `entities[0].properties.id`
    - `gatewaySerial` is `entities[0].entities[0].properties.serial`

3. Use above data to replace `{installationId}` and `{gatewaySerial}` in this URL to investigate the Viessmann API:

    `https://api.viessmann-platform.io/operational-data/v1/installations/{installationId}/gateways/{gatewaySerial}/devices/0/features`

## Types of heatings
- Use ViCareSession for gas heatings
- Use ViCareHeatPumpSession for heat pumps
