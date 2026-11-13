import unittest
from datetime import date, datetime, timedelta, timezone
from unittest.mock import Mock

from PyViCare.PyViCareService import ViCareDeviceAccessor, ViCareService
from PyViCare.PyViCareUtils import PyViCareInvalidDataError
from tests.helper import readJson

EVENTS_URL = '/events-history/installations/[id]/events'


class PyViCareServiceEventsTest(unittest.TestCase):

    def setUp(self):
        self.oauth_mock = Mock()
        self.oauth_mock.get.return_value = readJson('response/events/device-error.json')
        self.accessor = ViCareDeviceAccessor('[id]', '[serial]', '0')
        self.service = ViCareService(self.oauth_mock, [])

    def _url(self) -> str:
        return str(self.oauth_mock.get.call_args.args[0])

    def test_fetch_events_url(self):
        self.service.fetch_events(self.accessor)
        self.oauth_mock.get.assert_called_once_with(EVENTS_URL)

    def test_fetch_events_url_with_filters(self):
        self.service.fetch_events(self.accessor, 'device-error', limit=5)
        self.assertEqual(self._url(), f'{EVENTS_URL}?eventType=device-error&limit=5')

    def test_fetch_events_url_with_last_days(self):
        self.service.fetch_events(self.accessor, last_days=7)
        self.assertEqual(self._url(), f'{EVENTS_URL}?lastNDays=7')

    def test_fetch_events_url_with_since(self):
        self.service.fetch_events(self.accessor, since=datetime(2026, 10, 1))
        self.assertEqual(self._url(), f'{EVENTS_URL}?timestamp=2026-10-01T00%3A00%3A00Z')

    def test_fetch_events_url_with_since_aware(self):
        self.service.fetch_events(
            self.accessor,
            since=datetime(2026, 10, 18, 2, 0, 0, tzinfo=timezone(timedelta(hours=2))))
        self.assertEqual(self._url(), f'{EVENTS_URL}?timestamp=2026-10-18T00%3A00%3A00Z')

    def test_fetch_events_url_with_on_date(self):
        self.service.fetch_events(self.accessor, on_date=date(2026, 10, 17))
        self.assertEqual(self._url(), f'{EVENTS_URL}?date=2026-10-17')

    def test_fetch_events_url_with_gateway_serials(self):
        self.service.fetch_events(self.accessor, gateway_serials='7637415012096236')
        self.assertEqual(self._url(), f'{EVENTS_URL}?gatewaySerials=7637415012096236')

    def test_fetch_events_url_with_multiple_gateways(self):
        self.service.fetch_events(self.accessor, gateway_serials='1111,2222')
        self.assertEqual(self._url(), f'{EVENTS_URL}?gatewaySerials=1111%2C2222')

    def test_fetch_events_url_encodes_cursor(self):
        self.service.fetch_events(self.accessor, cursor='ab+cd==')
        self.assertEqual(self._url(), f'{EVENTS_URL}?cursor=ab%2Bcd%3D%3D')

    def test_fetch_events_url_with_multiple_types(self):
        self.service.fetch_events(self.accessor, 'device-error,device-message-warning')
        self.assertEqual(
            self._url(),
            f'{EVENTS_URL}?eventType=device-error%2Cdevice-message-warning')

    def test_fetch_events_rejects_two_windows(self):
        self.assertRaises(
            ValueError, self.service.fetch_events, self.accessor,
            None, last_days=7, since=datetime(2026, 10, 1))

    def test_fetch_events_rejects_invalid_last_days(self):
        self.assertRaises(ValueError, self.service.fetch_events, self.accessor, last_days=0)

    def test_fetch_events_rejects_limit_below_one(self):
        self.assertRaises(ValueError, self.service.fetch_events, self.accessor, limit=0)

    def test_fetch_events_rejects_negative_limit(self):
        self.assertRaises(ValueError, self.service.fetch_events, self.accessor, limit=-5)

    def test_fetch_events_clamps_limit(self):
        self.service.fetch_events(self.accessor, limit=5000)
        self.assertIn('limit=1000', self._url())

    def test_fetch_events_returns_typed_page(self):
        page = self.service.fetch_events(self.accessor)
        self.assertEqual(len(page.events), 2)
        self.assertEqual(page.events[0].error_code, 'f4')
        self.assertFalse(page.events[0].active)
        self.assertTrue(page.events[1].active)
        self.assertIsNone(page.next_cursor)

    def test_fetch_events_missing_data_raises(self):
        self.oauth_mock.get.return_value = {
            'statusCode': 400, 'errorType': 'VALIDATION_ERROR',
            'message': 'Some of the parameters are not correct'}
        self.assertRaises(
            PyViCareInvalidDataError,
            self.service.fetch_events, self.accessor)

    def test_fetch_events_non_dict_response_raises(self):
        self.oauth_mock.get.return_value = []
        self.assertRaises(
            PyViCareInvalidDataError,
            self.service.fetch_events, self.accessor)

    def test_fetch_events_uses_installation_not_device(self):
        other = ViCareDeviceAccessor('[id]', '[other-serial]', 'gateway')
        self.service.fetch_events(other)
        self.assertEqual(self._url(), EVENTS_URL)
