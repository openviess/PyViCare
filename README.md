# PyViCare

This library implements access to Viessmann devices by using the official API from the [Viessmann Developer Portal](https://developer.viessmann.com/).

## Breaking changes in version 2.8.x

- The circuit, burner (Gaz) and compressor (Heat Pump) is now separted. Accessing the properties of the burner/compressor is moved from `device.curcuits` to `device.burners` and `device.compressor`.

## Breaking changes in version 2.x

- The API to access your device changed to a general `PyViCare` class. Use this class to load all available devices.
- The API to access the heating circuit of the device has moved to the `Device` class. You can now access and iterate over all available circuits via `device.curcuits`. This allows to easily see which properties are depending on the circuit.

See the example below for how you can use that.

## Breaking changes in version 1.x

- The versions prior to 1.x used an inofficial API which stopped working on July, 15th 2021. All users need to migrate to version 1.0.0 to continue using the API.
- Exception is raised if the library runs into a API rate limit. (See feature flag `raise_exception_on_rate_limit`)
- Exception is raised if an unsupported device feature is used. (See feature flag `raise_exception_on_not_supported_device_feature`)
- Python 3.4 is no longer supported.
- Python 3.9 is now supported.

## Prerequisites

To use PyViCare, every user has to register and create their private API key. Follow these steps to create your API key:

1. Login to the [Viessmann Developer Portal](https://developer.viessmann.com/) with your existing ViCare username from the ViCare app.
2. In the menu navigate to `API Keys`.
3. Create a new OAuth client using following data:
   - Name: PyViCare
   - Google reCAPTCHA: Disabled
   - Redirect URIs: `vicare://oauth-callback/everest`
4. Copy the `Client ID` to use in your code. Pass it as constructor parameter to the device.

Please note that not all properties from older versions and the ViCare mobile app are available in the new API. Missing properties were removed and might be added later if they are available again.

## Help

We need help testing and improving PyViCare, since the maintainers only have specific types of heating systems. For bugs, questions or feature requests join the [PyViCare channel on Discord](https://discord.gg/aM3SqCD88f) or create an issue in this repository.

## Device Features / Errors

Depending on the device, some features are not available/supported. This results in a raising of a `PyViCareNotSupportedFeatureError` if the dedicated method is called. This is most likely not a bug, but a limitation of the device itself.

Tip: You can use Pythons [contextlib.suppress](https://docs.python.org/3/library/contextlib.html#contextlib.suppress) to handle it gracefully.

## Types of heatings

- Use `asGazBoiler` for gas heatings
- Use `asHeatPump` for heat pumps
- Use `asFuelCell` for fuel cells
- Use `asPelletsBoiler` for pellets heatings
- Use `asOilBoiler` for oil heatings
- Use `asHybridDevice` for gas/heat pump hybrid heatings

## Basic Usage:

```python
import sys
import logging
from PyViCare.PyViCare import PyViCare

client_id = "INSERT CLIENT ID"
email = "email@domain"
password = "password"

vicare = PyViCare()
vicare.initWithCredentials(email, password, client_id, "token.save")
device = vicare.devices[0]
print(device.getModel())
print("Online" if device.isOnline() else "Offline")

t = device.asAutoDetectDevice()
print(t.getDomesticHotWaterConfiguredTemperature())
print(t.getDomesticHotWaterStorageTemperature())
print(t.getOutsideTemperature())
print(t.getRoomTemperature())
print(t.getBoilerTemperature())
print(t.setDomesticHotWaterTemperature(59))

circuit = t.circuits[0] #select heating circuit

print(circuit.getSupplyTemperature())
print(circuit.getHeatingCurveShift())
print(circuit.getHeatingCurveSlope())

print(circuit.getActiveProgram())
print(circuit.getPrograms())

print(circuit.getCurrentDesiredTemperature())
print(circuit.getDesiredTemperatureForProgram("comfort"))
print(circuit.getActiveMode())

print(circuit.getDesiredTemperatureForProgram("comfort"))
print(circuit.setProgramTemperature("comfort",21))
print(circuit.activateProgram("comfort"))
print(circuit.deactivateComfort())

burner = t.burners[0] #select burner
print(burner.getActive())

compressor = t.compressors[0] #select compressor
print(compressor.getActive())

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

## Rate Limits

[Due to latest changes in the Viessmann API](https://www.viessmann-community.com/t5/Konnektivitaet/Q-amp-A-Viessmann-API/td-p/127660) rate limits can be hit. In that case a `PyViCareRateLimitError` is raised. You can read from the error (`limitResetDate`) when the rate limit is reset.

## More different devices for test cases needed

In order to help ensuring making it easier to create more test cases you can run this code and make a pull request with the new test of your device type added. Your test should be commited into [tests/response](tests/response) and named `<family><model>`.

The code to run to make this happen is below. This automatically removes "sensitive" information like installation id and serial numbers.
You can either replace default values or use the `PYVICARE_*` environment variables.

```python
import sys
import os
from PyViCare.PyViCare import PyViCare

client_id = os.getenv("PYVICARE_CLIENT_ID", "INSERT CLIENT_ID")
email = os.getenv("PYVICARE_EMAIL", "email@domain")
password = os.getenv("PYVICARE_PASSWORD", "password")

vicare = PyViCare()
vicare.initWithCredentials(email, password, client_id, "token.save")

with open(f"dump.json", mode='w') as output:
   output.write(vicare.devices[0].dump_secure())

```
