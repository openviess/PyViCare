# PyViCare

Implements an object to interact with the Viessmann ViCare API.
The OAuth2 authentication token can optionally be stored in a file to be reused.
Tokens are automatically renewed.

A few nice feature removed from the app are available though the API (Comfort and Eco modes).

## Version 0.1.0
Note that the version 0.1.0 DOES BREAK a few things.
`ViCareSession` is now removed.
You can now use the following objects:
```python
from PyViCare.PyViCareDevice import Device # generic device
from PyViCare.PyViCareGazBoiler import GazBoiler # gaz boiler
from PyViCare.PyViCareHeatPump import HeatPump # heat pump
```
## Version with PKCE
Note that the new API will break a lot! 
Only simple thing fixed sofar.
## Device Features / Errors

Depending on the device, some features are not available/supported. This results in a raising of a `PyViCareNotSupportedFeatureError` if the dedicated method is called. This is most likely not a bug, but a limitation of the device itself.

## Basic usage
Simple example:
```python
import sys
import logging
sys.path.insert(0, 'PyViCare')
from PyViCare.PyViCareGazBoiler import GazBoiler

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

Follow these steps to access the new API with PKCE in Postman:

1. Register API-Key at https://developer.viessmann.com/de/clients

    - add new client with any name
    - disable Google reCAPTCHA
    - use Redirect URI: `vicare://oauth-callback/everest`

2. Create an access token in the `Authorization` tab with type `OAuth 2.0` and following inputs:

    - Client id: from step 1
    - Callback url: `vicare://oauth-callback/everest`
    - Auth url: `https://iam.viessmann.com/idp/v1/authorize`
    - Access token url: `https://iam.viessmann.com/idp/v1/token`
    - Grant Type: Authorization Code (With PKCE)
    - Code Challenge Method: S256
    - Scope: `IoT user`
    - Client Authentication: in body
    - empty: Client Secret, Code Verifier, State
    A login popup will open. Enter your ViCare username and password. Preceed and use token

3. Use this URL to access your `installationId` and `gatewaySerial`: 

    `https://api.viessmann.com/iot/v1/equipment/installations`
    - `installationId` is `data[0].id`
    
    `https://api.viessmann.com/iot/v1/equipment/installations`
    - `gatewaySerial` is `data[0].serial`

4. Use above data to replace `{installationId}` and `{gatewaySerial}` in this URL to investigate the Viessmann API:

    `https://api.viessmann.com/iot/v1/equipment/installations/'+str(id)+'/gateways/'+str(serial)+'/devices/'+str(circuit)+'/features/'

## Types of heatings
- Use `GazBoiler` for gas heatings
- Use `HeatPump` for heat pumps
- Use `FuelCell` for fuel cells

## Rate Limits

[Due to latest changes in the Viessmann API](https://www.viessmann-community.com/t5/Konnektivitaet/Q-amp-A-Viessmann-API/td-p/127660) rate limits can be hit. In that case a `PyViCareRateLimitError` is raised. You can read from the error (`limitResetDate`) when the rate limit is reset.