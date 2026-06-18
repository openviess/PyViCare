"""End-to-end test: PyViCare in viaGateway mode shares one service per gateway.

Builds PyViCare with a mocked OAuth manager that serves
- the installations/gateways listing
- the bulk gateway features response (lifted from PR #626 fixtures)
and verifies that all devices on a gateway share a single bulk fetch.
"""
import unittest
from unittest.mock import Mock

from PyViCare.PyViCare import PyViCare
from PyViCare.PyViCareCachedServiceViaGateway import \
    ViCareCachedServiceViaGateway
from tests.helper import readJson


INSTALLATIONS_HEATBOX1 = {
    "data": [{
        "id": 1234567,
        "description": "Test Installation",
        "address": {"street": "Teststreet"},
        "gateways": [{
            "serial": "1234567812345678",
            "producedAt": "2024-01-01T00:00:00.000Z",
            "autoUpdate": True,
            "aggregatedStatus": "Online",
            "registeredAt": "2024-01-01T00:00:00.000Z",
            "devices": [
                {"id": "gateway", "modelId": "Heatbox1", "status": "Online",
                 "deviceType": "vitoconnect", "roles": ["type:gateway;VitoconnectOpto1"],
                 "createdAt": "2024-01-01T00:00:00.000Z"},
                {"id": "0", "modelId": "E3_Vitodens_300_W_B3HA", "status": "Online",
                 "deviceType": "heating", "roles": ["type:boiler", "type:E3"],
                 "createdAt": "2024-01-01T00:00:00.000Z"},
            ],
        }],
    }]
}


class PyViCareViaGatewayIntegrationTest(unittest.TestCase):

    def _build(self, installations, bulk_response):
        oauth = Mock()
        installations_url = "/equipment/installations?includeGateways=true"

        def get(url):
            if url == installations_url:
                return installations
            return bulk_response

        oauth.get.side_effect = get
        vicare = PyViCare()
        vicare.loadViaGateway(True)
        vicare.initWithExternalOAuth(oauth)
        return vicare, oauth

    def test_loadViaGateway_wires_gateway_service(self):
        bulk = readJson("response/gatewayWithDevices/heatbox1/Vitodens-300-W-B3HA.json")
        vicare, _ = self._build(INSTALLATIONS_HEATBOX1, bulk)
        # all devices on the gateway share the same service instance
        services = {id(d.service) for d in vicare.devices}
        self.assertEqual(len(services), 1)
        for device in vicare.devices:
            self.assertIsInstance(device.service, ViCareCachedServiceViaGateway)

    def test_devices_share_single_bulk_fetch(self):
        bulk = readJson("response/gatewayWithDevices/heatbox1/Vitodens-300-W-B3HA.json")
        vicare, oauth = self._build(INSTALLATIONS_HEATBOX1, bulk)

        # 1 installations call done during init
        installations_calls = sum(
            1 for c in oauth.get.call_args_list
            if c.args[0] == "/equipment/installations?includeGateways=true")
        self.assertEqual(installations_calls, 1)

        # Pick a feature that exists in the bulk response per device, then
        # request it from every device on the gateway. All getProperty calls
        # must hit the single shared cache → exactly one bulk fetch in total.
        per_device_feature = {}
        for entity in bulk["data"]:
            uri = entity.get("uri", "")
            if "/devices/" not in uri:
                continue
            dev_id = uri.split("/devices/")[1].split("/")[0]
            per_device_feature.setdefault(dev_id, entity["feature"])

        for device_config in vicare.devices:
            feature = per_device_feature.get(device_config.device_id)
            if feature is None:
                continue
            device_config.service.getProperty(device_config.accessor, feature)

        bulk_calls = sum(
            1 for c in oauth.get.call_args_list
            if c.args[0] != "/equipment/installations?includeGateways=true")
        self.assertEqual(bulk_calls, 1)

    def test_default_mode_uses_per_device_service(self):
        # Without loadViaGateway, behavior is unchanged: per-device cached service
        from PyViCare.PyViCareCachedService import ViCareCachedService
        oauth = Mock()
        oauth.get.return_value = INSTALLATIONS_HEATBOX1
        vicare = PyViCare()
        vicare.initWithExternalOAuth(oauth)
        for device in vicare.devices:
            self.assertIsInstance(device.service, ViCareCachedService)
        # different instances per device
        services = {id(d.service) for d in vicare.devices}
        self.assertEqual(len(services), len(vicare.devices))

    def test_bulk_response_isEnabled_features_are_visible_per_device(self):
        bulk = readJson("response/gatewayWithDevices/heatbox1/Vitodens-300-W-B3HA.json")
        vicare, _ = self._build(INSTALLATIONS_HEATBOX1, bulk)
        # The heating device should be able to read SOME feature that exists in the bulk
        # response for its device_id. Pick any feature with /devices/0/ in its uri.
        device_zero_features = [
            e["feature"] for e in bulk["data"]
            if "/devices/0/" in e.get("uri", "")
        ]
        self.assertGreater(len(device_zero_features), 0,
                           "fixture should contain features for device 0")
        heating = next(d for d in vicare.devices if d.device_id == "0")
        feature = heating.service.getProperty(heating.accessor, device_zero_features[0])
        self.assertEqual(feature["feature"], device_zero_features[0])
