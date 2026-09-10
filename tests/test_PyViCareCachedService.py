import unittest
from unittest.mock import Mock

from PyViCare.PyViCareCachedService import ViCareCachedService
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import (PyViCareDeviceCommunicationError,
                                    PyViCareInternalServerError,
                                    PyViCareInvalidDataError,
                                    PyViCareNotSupportedFeatureError,
                                    PyViCareRateLimitError)
from tests.helper import now_is


class PyViCareCachedServiceTest(unittest.TestCase):

    CACHE_DURATION = 60

    def setUp(self):
        self.oauth_mock = Mock()
        self.oauth_mock.get.return_value = {'data': [{"feature": "someprop"}]}
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "[device]")
        self.service = ViCareCachedService(
            self.oauth_mock, [], self.CACHE_DURATION)

    def test_fetch_all_features_is_cached(self):
        """fetch_all_features() must warm the cache, like the gateway variant.

        Callers that refresh with fetch_all_features() and then read properties
        would otherwise pay for two requests per interval.
        """
        with now_is('2000-01-01 00:00:00'):
            self.service.fetch_all_features(self.accessor)
            self.service.getProperty(self.accessor, "someprop")
        self.assertEqual(self.oauth_mock.get.call_count, 1)

    def test_getProperty_existing(self):
        self.service.getProperty(self.accessor, "someprop")
        self.oauth_mock.get.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/devices/[device]/features/')

    def test_getProperty_nonexisting_raises_exception(self):

        def func():
            return self.service.getProperty(self.accessor, "some-non-prop")
        self.assertRaises(PyViCareNotSupportedFeatureError, func)

    def test_setProperty_works(self):
        self.service.setProperty(self.accessor, "someotherprop", "doaction", {'name': 'abc'})
        self.oauth_mock.post.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/devices/[device]/features/someotherprop/commands/doaction', '{"name": "abc"}')

    def test_getProperty_existing_cached(self):
        # time+0 seconds
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty(self.accessor, "someprop")
            self.service.getProperty(self.accessor, "someprop")

        # time+30 seconds
        with now_is('2000-01-01 00:00:30'):
            self.service.getProperty(self.accessor, "someprop")

        self.assertEqual(self.oauth_mock.get.call_count, 1)
        self.oauth_mock.get.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/devices/[device]/features/')

        # time+70 seconds (must be more than CACHE_DURATION)
        with now_is('2000-01-01 00:01:10'):
            self.service.getProperty(self.accessor, "someprop")

        self.assertEqual(self.oauth_mock.get.call_count, 2)

    def test_setProperty_invalidateCache(self):
        # freeze time
        with now_is('2000-01-01 00:00:00'):
            self.assertEqual(self.service.is_cache_invalid(), True)
            self.service.getProperty(self.accessor, "someprop")
            self.assertEqual(self.service.is_cache_invalid(), False)

            self.service.setProperty(self.accessor,
                "someotherprop", "doaction", {'name': 'abc'})
            self.assertEqual(self.service.is_cache_invalid(), True)

            self.service.getProperty(self.accessor, "someprop")
            self.assertEqual(self.oauth_mock.get.call_count, 2)

    def test_device_communication_error_returns_stale_cache(self):
        """When device goes offline after successful fetch, return stale cache."""
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty(self.accessor, "someprop")

        # Device goes offline after cache expires
        self.oauth_mock.get.side_effect = PyViCareDeviceCommunicationError(
            {"errorType": "DEVICE_COMMUNICATION_ERROR",
             "extendedPayload": {"reason": "GATEWAY_OFFLINE"}})

        with now_is('2000-01-01 00:01:10'):
            result = self.service.getProperty(self.accessor, "someprop")

        self.assertIsNotNone(result)

    def test_server_error_returns_stale_cache(self):
        """When server returns 500 after successful fetch, return stale cache."""
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty(self.accessor, "someprop")

        self.oauth_mock.get.side_effect = PyViCareInternalServerError(
            {"statusCode": 500, "message": "Internal server error",
             "viErrorId": "test"})

        with now_is('2000-01-01 00:01:10'):
            result = self.service.getProperty(self.accessor, "someprop")

        self.assertIsNotNone(result)

    def test_device_communication_error_raises_without_cache(self):
        """When device is offline on first fetch (no cache), must raise."""
        self.oauth_mock.get.side_effect = PyViCareDeviceCommunicationError(
            {"errorType": "DEVICE_COMMUNICATION_ERROR",
             "extendedPayload": {"reason": "DEVICE_OFFLINE"}})

        with now_is('2000-01-01 00:00:00'):
            self.assertRaises(
                PyViCareDeviceCommunicationError,
                self.service.getProperty, self.accessor, "someprop")

    def test_server_error_raises_without_cache(self):
        """When server errors on first fetch (no cache), must raise."""
        self.oauth_mock.get.side_effect = PyViCareInternalServerError(
            {"statusCode": 500, "message": "Internal server error",
             "viErrorId": "test"})

        with now_is('2000-01-01 00:00:00'):
            self.assertRaises(
                PyViCareInternalServerError,
                self.service.getProperty, self.accessor, "someprop")

    def test_failed_fetch_is_not_retried_within_the_cache_window(self):
        """A failed fetch must cost one request, not one per reader.

        Every device on a gateway reads through the same service, so without
        this each of them would issue its own request for the rest of the
        window and burn the daily quota within the hour.
        """
        self.oauth_mock.get.side_effect = PyViCareDeviceCommunicationError(
            {"errorType": "DEVICE_COMMUNICATION_ERROR",
             "extendedPayload": {"reason": "DEVICE_OFFLINE"}})

        with now_is('2000-01-01 00:00:00'):
            for _ in range(5):
                self.assertRaises(
                    PyViCareDeviceCommunicationError,
                    self.service.getProperty, self.accessor, "someprop")

        with now_is('2000-01-01 00:00:30'):
            self.assertRaises(
                PyViCareDeviceCommunicationError,
                self.service.getProperty, self.accessor, "someprop")

        self.assertEqual(self.oauth_mock.get.call_count, 1)

        # the window is over, one more request is due
        with now_is('2000-01-01 00:01:10'):
            self.assertRaises(
                PyViCareDeviceCommunicationError,
                self.service.getProperty, self.accessor, "someprop")

        self.assertEqual(self.oauth_mock.get.call_count, 2)

    def test_rate_limit_is_replayed_within_the_cache_window(self):
        """Hitting the limit must not keep spending requests against it."""
        self.oauth_mock.get.side_effect = PyViCareRateLimitError(
            {"extendedPayload": {"name": "portal", "requestCountLimit": 3000,
                                 "limitReset": 946771204000}})

        with now_is('2000-01-01 00:00:00'):
            for _ in range(5):
                self.assertRaises(
                    PyViCareRateLimitError,
                    self.service.getProperty, self.accessor, "someprop")

        self.assertEqual(self.oauth_mock.get.call_count, 1)

    def test_invalid_data_leaves_the_stale_cache_readable(self):
        """A malformed response must not hide data we already hold."""
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty(self.accessor, "someprop")

        self.oauth_mock.get.return_value = {"unexpected": "response"}

        with now_is('2000-01-01 00:01:10'):
            self.assertRaises(
                PyViCareInvalidDataError,
                self.service.getProperty, self.accessor, "someprop")
            self.assertIsNotNone(
                self.service.getProperty(self.accessor, "someprop"))

        self.assertEqual(self.oauth_mock.get.call_count, 2)

    def test_failed_fetch_recovers_when_the_api_returns(self):
        self.oauth_mock.get.side_effect = PyViCareInternalServerError(
            {"statusCode": 500, "message": "Internal server error",
             "viErrorId": "test"})

        with now_is('2000-01-01 00:00:00'):
            self.assertRaises(
                PyViCareInternalServerError,
                self.service.getProperty, self.accessor, "someprop")

        self.oauth_mock.get.side_effect = None

        with now_is('2000-01-01 00:01:10'):
            self.assertIsNotNone(
                self.service.getProperty(self.accessor, "someprop"))

    def test_clear_cache_retries_immediately(self):
        """clear_cache() is an explicit request for fresh data."""
        self.oauth_mock.get.side_effect = PyViCareDeviceCommunicationError(
            {"errorType": "DEVICE_COMMUNICATION_ERROR",
             "extendedPayload": {"reason": "DEVICE_OFFLINE"}})

        with now_is('2000-01-01 00:00:00'):
            self.assertRaises(
                PyViCareDeviceCommunicationError,
                self.service.getProperty, self.accessor, "someprop")
            self.service.clear_cache()
            self.assertRaises(
                PyViCareDeviceCommunicationError,
                self.service.getProperty, self.accessor, "someprop")

        self.assertEqual(self.oauth_mock.get.call_count, 2)

    def test_invalid_data_still_raises_with_cache(self):
        """PyViCareInvalidDataError (genuine bad data) must still raise even with cache."""
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty(self.accessor, "someprop")

        self.oauth_mock.get.side_effect = None
        self.oauth_mock.get.return_value = {"unexpected": "response"}

        with now_is('2000-01-01 00:01:10'):
            self.assertRaises(
                PyViCareInvalidDataError,
                self.service.getProperty, self.accessor, "someprop")
