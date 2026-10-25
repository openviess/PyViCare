import unittest
from datetime import UTC, datetime, timedelta, timezone

from PyViCare.PyViCareEvent import ViCareEvent, ViCareEventPage
from PyViCare.PyViCareService import format_query_datetime
from tests.helper import readJson


class ViCareEventTest(unittest.TestCase):

    def setUp(self):
        self.payload = readJson('response/events/device-error.json')

    def test_cleared_event(self):
        event = ViCareEvent(self.payload['data'][0])
        self.assertEqual(event.event_type, 'device-error')
        self.assertEqual(event.gateway_serial, '[serial]')
        self.assertEqual(event.device_id, '0')
        self.assertEqual(event.model_id, 'VPlusHO1_4')
        self.assertEqual(event.error_code, 'f4')
        self.assertEqual(event.error_description, 'Keine Flammenbildung')
        self.assertEqual(event.error_event_type, 'Error')
        self.assertEqual(event.equipment_type, 'Boiler')
        self.assertFalse(event.active)
        self.assertIs(event.raw, self.payload['data'][0])

    def test_active_event(self):
        event = ViCareEvent(self.payload['data'][1])
        self.assertTrue(event.active)
        self.assertEqual(event.error_code, 'f4')

    def test_timestamp_is_timezone_aware_utc(self):
        event = ViCareEvent(self.payload['data'][0])
        expected = datetime(2026, 10, 17, 5, 1, 56, tzinfo=UTC)
        self.assertEqual(event.event_timestamp, expected)
        self.assertEqual(event.created_at, datetime(2026, 10, 17, 5, 2, 26, 803000, tzinfo=UTC))

    def test_invalid_timestamp_is_none(self):
        self.assertIsNone(ViCareEvent({'eventTimestamp': 'yesterday'}).event_timestamp)

    def test_missing_fields_are_tolerated(self):
        event = ViCareEvent({})
        self.assertEqual(event.event_type, '')
        self.assertIsNone(event.device_id)
        self.assertIsNone(event.error_code)
        self.assertFalse(event.active)
        self.assertIsNone(event.event_timestamp)

    def test_missing_body_is_tolerated(self):
        event = ViCareEvent({'eventType': 'device-error', 'body': None})
        self.assertIsNone(event.device_id)
        self.assertFalse(event.active)

    def test_page_with_cursor(self):
        payload = readJson('response/events/device-error-multi-device.json')
        page = ViCareEventPage.from_payload(payload)
        self.assertEqual(len(page.events), 2)
        self.assertEqual(page.next_cursor, 'NDcyZWQxNzRmNmYwNTQxNjk0NTg5ZGNiOGMyMzY0MjkwODUwODkwMQ==')
        self.assertEqual([e.device_id for e in page.events], ['gateway', '0'])

    def test_page_last_page_has_no_cursor(self):
        page = ViCareEventPage.from_payload(self.payload)
        self.assertIsNone(page.next_cursor)

    def test_page_empty(self):
        page = ViCareEventPage.from_payload({'cursor': {'next': ''}, 'data': []})
        self.assertEqual(page.events, [])
        self.assertIsNone(page.next_cursor)

    def test_page_skips_non_dict_entries(self):
        page = ViCareEventPage.from_payload({'data': [{'eventType': 'device-error'}, 'junk']})
        self.assertEqual(len(page.events), 1)

    def test_page_without_cursor_key(self):
        page = ViCareEventPage.from_payload({'data': []})
        self.assertIsNone(page.next_cursor)


class QueryDatetimeTest(unittest.TestCase):

    def test_none_passes_through(self):
        self.assertIsNone(format_query_datetime(None))

    def test_string_passes_through(self):
        self.assertEqual(format_query_datetime('2026-10-01T00:00:00Z'), '2026-10-01T00:00:00Z')

    def test_naive_datetime_is_utc(self):
        self.assertEqual(format_query_datetime(datetime(2026, 10, 1)), '2026-10-01T00:00:00Z')

    def test_aware_datetime_is_converted(self):
        value = datetime(2026, 10, 18, 2, 0, 0, tzinfo=timezone(timedelta(hours=2)))
        self.assertEqual(format_query_datetime(value), '2026-10-18T00:00:00Z')
