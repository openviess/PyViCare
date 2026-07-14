import unittest
from unittest.mock import Mock

from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareServiceViaGateway import (
    ViCareServiceViaGateway, filter_features_for_device)
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError


class PyViCareServiceViaGatewayTest(unittest.TestCase):

    BULK_RESPONSE = {
        "data": [
            {
                "feature": "device.serial",
                "uri": "https://api.viessmann.com/iot/v2/features/installations/[id]/gateways/[serial]/devices/[dev1]/features/device.serial",
                "isEnabled": True,
            },
            {
                "feature": "device.messages.errors.raw",
                "uri": "https://api.viessmann.com/iot/v2/features/installations/[id]/gateways/[serial]/devices/[dev1]/features/device.messages.errors.raw",
                "isEnabled": True,
            },
            {
                "feature": "device.serial",
                "uri": "https://api.viessmann.com/iot/v2/features/installations/[id]/gateways/[serial]/devices/[dev2]/features/device.serial",
                "isEnabled": True,
            },
        ]
    }

    def setUp(self):
        self.oauth_mock = Mock()
        self.oauth_mock.get.return_value = self.BULK_RESPONSE
        self.service = ViCareServiceViaGateway(self.oauth_mock)
        self.accessor1 = ViCareDeviceAccessor("[id]", "[serial]", "[dev1]")
        self.accessor2 = ViCareDeviceAccessor("[id]", "[serial]", "[dev2]")

    def test_fetch_all_features_uses_bulk_url(self):
        self.service.fetch_all_features(self.accessor1)
        self.oauth_mock.get.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/features?includeDevicesFeatures=true')

    def test_getProperty_filters_to_caller_device(self):
        feature = self.service.getProperty(self.accessor1, "device.serial")
        self.assertIn("[dev1]", feature["uri"])

    def test_getProperty_finds_feature_for_each_device(self):
        f1 = self.service.getProperty(self.accessor1, "device.serial")
        f2 = self.service.getProperty(self.accessor2, "device.serial")
        self.assertIn("[dev1]", f1["uri"])
        self.assertIn("[dev2]", f2["uri"])

    def test_getProperty_missing_feature_raises(self):
        self.assertRaises(
            PyViCareNotSupportedFeatureError,
            self.service.getProperty, self.accessor1, "does.not.exist")

    def test_getProperty_missing_feature_for_other_device_raises(self):
        # device.messages.errors.raw exists only for dev1; dev2 must raise
        self.assertRaises(
            PyViCareNotSupportedFeatureError,
            self.service.getProperty, self.accessor2, "device.messages.errors.raw")

    def test_setProperty_uses_per_device_url(self):
        self.service.setProperty(self.accessor1, "x.y", "doaction", {"a": 1})
        self.oauth_mock.post.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/devices/[dev1]/features/x.y/commands/doaction',
            '{"a": 1}')

    def test_filter_features_for_device_handles_missing_uri(self):
        entities = [{"feature": "x"}, {"feature": "y", "uri": "/devices/[dev1]/features/y"}]
        result = filter_features_for_device(entities, "[dev1]")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["feature"], "y")
