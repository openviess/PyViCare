import unittest
from unittest.mock import Mock

from PyViCare.PyViCareCachedServiceViaGateway import \
    ViCareCachedServiceViaGateway
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import (PyViCareDeviceCommunicationError,
                                    PyViCareInternalServerError,
                                    PyViCareInvalidDataError,
                                    PyViCareNotSupportedFeatureError)
from tests.helper import now_is


BULK_RESPONSE = {
    "data": [
        {
            "feature": "device.serial",
            "uri": "https://api.viessmann.com/iot/v2/features/installations/[id]/gateways/[serial]/devices/[dev1]/features/device.serial",
            "isEnabled": True,
        },
        {
            "feature": "device.serial",
            "uri": "https://api.viessmann.com/iot/v2/features/installations/[id]/gateways/[serial]/devices/[dev2]/features/device.serial",
            "isEnabled": True,
        },
    ]
}


class PyViCareCachedServiceViaGatewayTest(unittest.TestCase):

    CACHE_DURATION = 60

    def setUp(self):
        self.oauth_mock = Mock()
        self.oauth_mock.get.return_value = BULK_RESPONSE
        self.service = ViCareCachedServiceViaGateway(
            self.oauth_mock, self.CACHE_DURATION)
        self.accessor1 = ViCareDeviceAccessor("[id]", "[serial]", "[dev1]")
        self.accessor2 = ViCareDeviceAccessor("[id]", "[serial]", "[dev2]")

    def test_fetch_all_features_is_cached(self):
        """Coordinators calling fetch_all_features() directly must share the cache.

        This is the critical optimization for HA's per-device DataUpdateCoordinator
        pattern: each coordinator does clear_cache + fetch_all_features per refresh.
        In gateway mode there is one bulk endpoint per gateway, so concurrent
        fetch_all_features calls must collapse to a single HTTP call.
        """
        with now_is('2000-01-01 00:00:00'):
            r1 = self.service.fetch_all_features(self.accessor1)
            r2 = self.service.fetch_all_features(self.accessor2)
            r3 = self.service.fetch_all_features(self.accessor1)
        self.assertEqual(self.oauth_mock.get.call_count, 1)
        self.assertEqual(r1, r2)
        self.assertEqual(r1, r3)

    def test_two_devices_share_single_bulk_fetch(self):
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty(self.accessor1, "device.serial")
            self.service.getProperty(self.accessor2, "device.serial")
            self.service.getProperty(self.accessor1, "device.serial")
        self.assertEqual(self.oauth_mock.get.call_count, 1)
        self.oauth_mock.get.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/features?includeDevicesFeatures=true')

    def test_cache_respects_TTL(self):
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty(self.accessor1, "device.serial")
        with now_is('2000-01-01 00:00:30'):
            self.service.getProperty(self.accessor1, "device.serial")
        self.assertEqual(self.oauth_mock.get.call_count, 1)
        with now_is('2000-01-01 00:01:10'):
            self.service.getProperty(self.accessor1, "device.serial")
        self.assertEqual(self.oauth_mock.get.call_count, 2)

    def test_setProperty_invalidates_cache_for_all_devices(self):
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty(self.accessor1, "device.serial")
            self.service.getProperty(self.accessor2, "device.serial")
            self.assertEqual(self.oauth_mock.get.call_count, 1)
            self.assertEqual(self.service.is_cache_invalid(), False)

            self.service.setProperty(self.accessor1, "x.y", "doaction", {"a": 1})
            self.assertEqual(self.service.is_cache_invalid(), True)

            self.service.getProperty(self.accessor2, "device.serial")
            self.assertEqual(self.oauth_mock.get.call_count, 2)

    def test_getProperty_filters_to_caller_device(self):
        with now_is('2000-01-01 00:00:00'):
            f1 = self.service.getProperty(self.accessor1, "device.serial")
            f2 = self.service.getProperty(self.accessor2, "device.serial")
        self.assertIn("[dev1]", f1["uri"])
        self.assertIn("[dev2]", f2["uri"])

    def test_getProperty_missing_raises(self):
        self.assertRaises(
            PyViCareNotSupportedFeatureError,
            self.service.getProperty, self.accessor1, "no.such.feature")

    def test_device_communication_error_returns_stale_cache(self):
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty(self.accessor1, "device.serial")

        self.oauth_mock.get.side_effect = PyViCareDeviceCommunicationError(
            {"errorType": "DEVICE_COMMUNICATION_ERROR",
             "extendedPayload": {"reason": "GATEWAY_OFFLINE"}})

        with now_is('2000-01-01 00:01:10'):
            result = self.service.getProperty(self.accessor1, "device.serial")
        self.assertIsNotNone(result)

    def test_server_error_returns_stale_cache(self):
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty(self.accessor1, "device.serial")

        self.oauth_mock.get.side_effect = PyViCareInternalServerError(
            {"statusCode": 500, "message": "Internal server error",
             "viErrorId": "test"})

        with now_is('2000-01-01 00:01:10'):
            result = self.service.getProperty(self.accessor1, "device.serial")
        self.assertIsNotNone(result)

    def test_device_communication_error_raises_without_cache(self):
        self.oauth_mock.get.side_effect = PyViCareDeviceCommunicationError(
            {"errorType": "DEVICE_COMMUNICATION_ERROR",
             "extendedPayload": {"reason": "DEVICE_OFFLINE"}})

        with now_is('2000-01-01 00:00:00'):
            self.assertRaises(
                PyViCareDeviceCommunicationError,
                self.service.getProperty, self.accessor1, "device.serial")

    def test_invalid_data_still_raises_with_cache(self):
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty(self.accessor1, "device.serial")

        self.oauth_mock.get.side_effect = None
        self.oauth_mock.get.return_value = {"unexpected": "response"}

        with now_is('2000-01-01 00:01:10'):
            self.assertRaises(
                PyViCareInvalidDataError,
                self.service.getProperty, self.accessor1, "device.serial")
