# PyViCare

This library implements access to Viessmann devices by using the official API from the [Viessmann Developer Portal](https://developer.viessmann.com/).

## Breaking changes in version 1.x

* The versions prior to 1.x used an inofficial API which stopped working on July, 15th 2021. All users need to migrate to version 1.0.0 to continue using the API.
* Exception is raised if the library runs into a API rate limit.  (See feature flag `raise_exception_on_rate_limit`)
* Exception is raised if an unsupported device feature is used. (See feature flag `raise_exception_on_not_supported_device_feature`)
* Python 3.4 is no longer supported.
* Python 3.9 is now supported.

## Help

We need help testing and improving PyViCare, since the maintainers only have specific types of heating systems. For bugs, questions or feature requests join the [PyViCare channel on Discord](https://discord.gg/aM3SqCD88f) or create an issue in this repository.

## Device Features / Errors

Depending on the device, some features are not available/supported. This results in a raising of a `PyViCareNotSupportedFeatureError` if the dedicated method is called. This is most likely not a bug, but a limitation of the device itself.

## Types of heatings
- Use `GazBoiler` for gas heatings
- Use `HeatPump` for heat pumps
- Use `FuelCell` for fuel cells

## Basic Usage:

```python
import sys
import logging
sys.path.insert(0, 'PyViCare')
from PyViCare.PyViCareGazBoiler import GazBoiler

client_id = "INSERT CLIENT ID"

t=GazBoiler("email@domain","password","token.save", 0, 60, client_id=client_id)
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

## API Usage in Postman

Follow these steps to access the API in Postman:

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

2. Use this URL to access your `installationId` and `gatewaySerial`: 

    `https://api.viessmann.com/iot/v1/equipment/installations?includeGateways=true`

    - `installationId` is `data[0].id`
    - `gatewaySerial` is `data[0].gateways[0].serial`

3. Use above data to replace `{installationId}` and `{gatewaySerial}` in this URL to investigate the Viessmann API:

    `https://api.viessmann.com/iot/v1/equipment/installations/{installationId}/gateways/{gatewaySerial}/devices/0/features`


## Migrate to PyViCare 1.x

To use PyViCare 1.x, every user has to register and create their private API key. Follow these steps to create your API key:

1. Register and login in the [Viessmann Developer Portal](https://developer.viessmann.com/).
2. In the menu navigate to `API Keys`.
3. Create a new OAuth client using following data:
    * Name: PyViCare
    * Google reCAPTCHA: Disabled
    * Redirect URIs: `vicare://oauth-callback/everest`
4. Copy the `Client ID` to use in your code. Pass it as constructor parameter to the device.

Please not that not all previous properties are available in the new API. Missing properties were removed and might be added later if they are available again. 

## Rate Limits

[Due to latest changes in the Viessmann API](https://www.viessmann-community.com/t5/Konnektivitaet/Q-amp-A-Viessmann-API/td-p/127660) rate limits can be hit. In that case a `PyViCareRateLimitError` is raised. You can read from the error (`limitResetDate`) when the rate limit is reset.
