import unittest
from unittest.mock import Mock

from PyViCare.PyViCareCachedService import ViCareCachedService
from PyViCare.PyViCareCachedServiceViaGateway import ViCareCachedServiceViaGateway
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import (
    PyViCareInternalServerError,
    PyViCareRateLimitError,
)
from tests.helper import now_is, readJson

FEATURE_PAYLOAD = {
    "data": [
        {
            "feature": "someprop",
            "uri": "https://api.viessmann-climatesolutions.com/iot/v2/features/installations/[id]/gateways/[serial]/devices/0/features/someprop",
            "properties": {"value": {"type": "number", "value": 1}},
        }
    ]
}


class PyViCareCachedServiceEventsTest(unittest.TestCase):

    CACHE_DURATION = 60

    def setUp(self):
        self.oauth_mock = Mock()
        self.oauth_mock.get.side_effect = self._answer
        self.accessor = ViCareDeviceAccessor('[id]', '[serial]', '0')
        self.service = ViCareCachedService(self.oauth_mock, [], self.CACHE_DURATION)

    def _answer(self, url):
        if url.startswith('/events-history/'):
            return readJson('response/events/device-error.json')
        return FEATURE_PAYLOAD

    def _event_calls(self) -> int:
        return sum(
            1 for call in self.oauth_mock.get.call_args_list
            if call.args[0].startswith('/events-history/'))

    def test_fetch_events_is_cached(self):
        with now_is('2000-01-01 00:00:00'):
            first = self.service.fetch_events(self.accessor)
            second = self.service.fetch_events(self.accessor)

        self.assertEqual(self._event_calls(), 1)
        self.assertIs(first, second)

    def test_fetch_events_respects_ttl(self):
        with now_is('2000-01-01 00:00:00'):
            self.service.fetch_events(self.accessor)
        with now_is('2000-01-01 00:00:30'):
            self.service.fetch_events(self.accessor)
        self.assertEqual(self._event_calls(), 1)

        with now_is('2000-01-01 00:01:10'):
            self.service.fetch_events(self.accessor)
        self.assertEqual(self._event_calls(), 2)

    def test_events_and_features_do_not_share_a_cache_slot(self):
        with now_is('2000-01-01 00:00:00'):
            page = self.service.fetch_events(self.accessor)
            feature = self.service.getProperty(self.accessor, "someprop")

        self.assertEqual(len(page.events), 2)
        self.assertEqual(feature["feature"], "someprop")
        self.assertEqual(self._event_calls(), 1)
        self.assertEqual(self.oauth_mock.get.call_count, 2)

    def test_different_limit_is_a_different_cache_entry(self):
        with now_is('2000-01-01 00:00:00'):
            self.service.fetch_events(self.accessor, limit=2)
            self.service.fetch_events(self.accessor, limit=2)
            self.service.fetch_events(self.accessor, limit=10)

        self.assertEqual(self._event_calls(), 2)

    def test_cursor_pages_bypass_the_cache(self):
        # a cursor is used once, keeping the page around would grow the cache
        with now_is('2000-01-01 00:00:00'):
            self.service.fetch_events(self.accessor, limit=2, cursor='abc')
            self.service.fetch_events(self.accessor, limit=2, cursor='abc')

        self.assertEqual(self._event_calls(), 2)

    def test_first_page_stays_cached_after_paging(self):
        with now_is('2000-01-01 00:00:00'):
            first = self.service.fetch_events(self.accessor, limit=2)
            self.service.fetch_events(self.accessor, limit=2, cursor='abc')
            again = self.service.fetch_events(self.accessor, limit=2)

        self.assertEqual(self._event_calls(), 2)
        self.assertIs(first, again)

    def test_server_error_returns_stale_events(self):
        with now_is('2000-01-01 00:00:00'):
            self.service.fetch_events(self.accessor)

        self.oauth_mock.get.side_effect = PyViCareInternalServerError(
            {"statusCode": 500, "message": "Internal server error", "viErrorId": "test"})

        with now_is('2000-01-01 00:01:10'):
            page = self.service.fetch_events(self.accessor)

        self.assertEqual(len(page.events), 2)

    def test_rate_limit_propagates(self):
        self.oauth_mock.get.side_effect = PyViCareRateLimitError(
            {"extendedPayload": {"name": "rate", "requestCountLimit": 1450, "limitReset": 1000}})

        with now_is('2000-01-01 00:00:00'):
            self.assertRaises(
                PyViCareRateLimitError,
                self.service.fetch_events, self.accessor)

    def test_clear_cache_drops_events(self):
        with now_is('2000-01-01 00:00:00'):
            self.service.fetch_events(self.accessor)
            self.service.clear_cache()
            self.service.fetch_events(self.accessor)

        self.assertEqual(self._event_calls(), 2)

    def test_events_and_features_are_cleared_together(self):
        with now_is('2000-01-01 00:00:00'):
            self.service.fetch_events(self.accessor)
            self.service.fetch_all_features(self.accessor)
            self.service.setProperty(self.accessor, "someprop", "doaction", {})
            self.service.fetch_events(self.accessor)
            self.service.fetch_all_features(self.accessor)

        self.assertEqual(self._event_calls(), 2)


class PyViCareCachedGatewayServiceEventsTest(unittest.TestCase):

    def setUp(self):
        self.oauth_mock = Mock()
        self.oauth_mock.get.side_effect = lambda url: readJson('response/events/device-error-multi-device.json')
        self.service = ViCareCachedServiceViaGateway(self.oauth_mock, 60)
        self.accessor0 = ViCareDeviceAccessor('[id]', '[serial]', '0')
        self.accessor_gateway = ViCareDeviceAccessor('[id]', '[serial]', 'gateway')

    def test_devices_on_the_same_gateway_share_one_events_fetch(self):
        with now_is('2000-01-01 00:00:00'):
            page0 = self.service.fetch_events(self.accessor0)
            page_gateway = self.service.fetch_events(self.accessor_gateway)

        self.assertEqual(self.oauth_mock.get.call_count, 1)
        self.assertIs(page0, page_gateway)

    def test_gateway_and_device_events_are_both_in_the_page(self):
        page = self.service.fetch_events(self.accessor0)
        self.assertEqual({event.device_id for event in page.events}, {'0', 'gateway'})

    def test_url_matches_gateway_service_conventions(self):
        self.service.fetch_events(self.accessor0)
        self.assertEqual(
            self.oauth_mock.get.call_args.args[0],
            '/events-history/installations/[id]/events')
