import unittest
from unittest.mock import Mock

from PyViCare.PyViCareHeatingDevice import HeatingCircuit, HeatingDevice
from PyViCare.PyViCareService import ViCareDeviceAccessor, ViCareService
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError

FEATURE = {
    "feature": "heating.circuits.0.operating.programs.normal",
    "properties": {"active": {"type": "boolean", "value": True}},
}
NOT_FOUND = {
    "viErrorId": "[id]",
    "statusCode": 404,
    "errorType": "FEATURE_NOT_FOUND",
    "message": "Feature not found",
    "extendedPayload": {},
}


class PyViCareServiceTest(unittest.TestCase):

    def setUp(self):
        self.oauth_mock = Mock()
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "[device]")
        self.service = ViCareService(self.oauth_mock, [])

    def test_getProperty(self):
        self.oauth_mock.get.return_value = {"data": FEATURE}
        self.assertEqual(self.service.getProperty(self.accessor, "someprop"), FEATURE)
        self.oauth_mock.get.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/devices/[device]/features/someprop')

    def test_getProperty_not_found(self):
        self.oauth_mock.get.return_value = NOT_FOUND
        with self.assertRaises(PyViCareNotSupportedFeatureError):
            self.service.getProperty(self.accessor, "someprop")

    def test_getPrograms_lists_only_existing_programs(self):
        def get(url):
            if url.endswith("heating.circuits.0.operating.programs.normal"):
                return {"data": FEATURE}
            return NOT_FOUND
        self.oauth_mock.get.side_effect = get
        circuit = HeatingCircuit(HeatingDevice(self.accessor, self.service), "0")
        self.assertEqual(circuit.getPrograms(), ["normal"])

    def test_setProperty_object(self):
        self.service.setProperty(self.accessor, "someprop", "doaction", {'name': 'abc'})
        self.oauth_mock.post.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/devices/[device]/features/someprop/commands/doaction', '{"name": "abc"}')

    def test_setProperty_string(self):
        self.service.setProperty(self.accessor, "someprop", "doaction", '{}')
        self.oauth_mock.post.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/devices/[device]/features/someprop/commands/doaction', '{}')

    def test_getProperty_gateway(self):
        self.service = ViCareService(self.oauth_mock, ["type:gateway;VitoconnectOpto1"])
        self.oauth_mock.get.return_value = {"data": FEATURE}
        self.service.getProperty(self.accessor, "someprop")
        self.oauth_mock.get.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/features/someprop')

    def test_fetch_all_features_gateway(self):
        self.service = ViCareService(self.oauth_mock, ["type:gateway;VitoconnectOpto1"])
        self.service.fetch_all_features(self.accessor)
        self.oauth_mock.get.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/features/')
