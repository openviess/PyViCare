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

# Viessmann V2 API

On July 15th the current Viessmann V1 API will be turned off. This library supports the Viessmann V2 API but not all properties are available (yet).

We need help testing the new V2 API. Please follow these steps to test the new API.

1. Register and login in the new [Viessmann Developer Portal](https://developer.viessmann.com/).
2. In the menu navigate to `API Keys`.
3. Create a new OAuth client using following data:
    * Name: PyViCare
    * Google reCAPTCHA: Disabled
    * Redirect URIs: `vicare://oauth-callback/everest`
4. Copy the `Client ID` to use in your code. Pass it as constructor parameter to the device.

## Basic Usage with V2:

```python
import sys
import logging
sys.path.insert(0, 'PyViCare')
from PyViCare.PyViCareGazBoiler import GazBoiler

client_id = "INSERT CLIENT ID"

t=GazBoiler("email@domain","password","token.save", client_id=client_id, useV2=True)
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

## API V2 Usage in Postman

Follow these steps to access the V2 API in Postman:

1. Create an access token in the `Authorization` tab with type `OAuth 2.0` and following inputs:

    - Token Name: `PyViCare`
    - Grant Type: `Authorization Code (With PKCE)`
    - Callback URL: `vicare://oauth-callback/everest`
    - Authorize using browser: Disabled
    - Auth URL: `https://iam.viessmann.com/idp/v2/authorize`
    - Access Token URL: `https://iam.viessmann.com/idp/v2/token`
    - Client ID: Your personal Client ID created in the developer portal.
    - Client Secret: Blank
    - Code Challenge Method: `SHA-256`
    - Code Veriefier: Blank
    - Scope: `IoT User`
    - State: Blank
    - Client Authentication: `Send client credentials in body`.

    A login popup will open. Enter your ViCare username and password.

2. Use this URL to access your `installationId`: 

    `https://api.viessmann.com/iot/v1/equipment/installations`

    - `installationId` is `data[0].id`

2. Use this URL to access your `gatewaySerial`. Replace `{installationId}` with the installation id above.

    `https://api.viessmann.com/iot/v1/equipment/installations/{installationId}/gateways`

    - `gatewaySerial` is `data[0].serial`

3. Use above data to replace `{installationId}` and `{gatewaySerial}` in this URL to investigate the Viessmann API:

    `https://api.viessmann.com/iot/v1/equipment/installations/{installationId}/gateways/{gatewaySerial}/devices/0/features`
