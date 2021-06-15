# PyViCare

Implements an object to interact with the Viessmann ViCare API.
The OAuth2 authentication token can optionally be stored in a file to be reused.
Tokens are automatically renewed.

This is a version adopted from somm15/PyViCare that changes the retrieval process. It doesn't create an url for each property,
which is bouncing up the connection counter to the Viessmann ViCare API ending up in an rate limit exception,
but does a retrieval of the whole data structure within one request.
For debugging purposes you can cache the data in a file and always read from this file as long as it exists

A few nice feature removed from the app are available though the API (Comfort and Eco modes).
The Solar properties are also available though the API.

## Version 0.1.0
Note that the version 0.1.0 DOES BREAK a few things.
`ViCareSession` is now removed.
You can now use the following objects:
```python
from PyViCare.PyViCareDevice import Device # generic device
from PyViCare.PyViCareGazBoiler import GazBoiler # gaz boiler
from PyViCare.PyViCareHeatPump import HeatPump # heat pump
```

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
t.getAllProperties(cache=True)  # for debugging use cache=True in order to save API calls
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

print(t.getSolarStorageTemperature())
print(t.getSolarCollectorTemperature())
print(t.getSolarPowerCumulativeProduced())
print(t.getSolarRechargeSuppression())
print(t.getSolarPowerProduction())
print(t.getSolarPumpActive())
print(t.getSolarHours())

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

    - Client id: `79742319e39245de5f91d15ff4cac2a8`
    - Secret id: `8ad97aceb92c5892e102b093c7c083fa`
    - Callback url: `vicare://oauth-callback/everest`
    - Auth url: `https://iam.viessmann.com/idp/v1/authorize`
    - Access token url: `https://iam.viessmann.com/idp/v1/token`
    - Scope: `openid`

    A login popup will open. Enter your ViCare username and password.

2. Use this URL to access your `installationId` and `gatewaySerial`: 

    `https://api.viessmann-platform.io/general-management/installations`

    - `installationId` is `entities[0].properties.id`
    - `gatewaySerial` is `entities[0].entities[0].properties.serial`

3. Use above data to replace `{installationId}` and `{gatewaySerial}` in this URL to investigate the Viessmann API:

    `https://api.viessmann-platform.io/operational-data/v1/installations/{installationId}/gateways/{gatewaySerial}/devices/0/features`

## Types of heatings
- Use `GazBoiler` for gas heatings
- Use `HeatPump` for heat pumps
- Use `FuelCell` for fuel cells

## Rate Limits

[Due to latest changes in the Viessmann API](https://www.viessmann-community.com/t5/Konnektivitaet/Q-amp-A-Viessmann-API/td-p/127660) rate limits can be hit. In that case a `PyViCareRateLimitError` is raised. You can read from the error (`limitResetDate`) when the rate limit is reset.
