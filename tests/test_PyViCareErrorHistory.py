import json
import unittest
from typing import Any

from PyViCare.PyViCareErrorHistory import ViCareErrorHistory, chronological
from PyViCare.PyViCareEvent import ViCareEvent
from tests.helper import readJson


def error_event(error_code: str, active: bool, timestamp: str | None,
                device_id: str = '0', created_at: str | None = None) -> ViCareEvent:
    raw: dict[str, Any] = {
        'eventType': 'device-error',
        'body': {'errorCode': error_code, 'deviceId': device_id, 'active': active},
    }
    if timestamp is not None:
        raw['eventTimestamp'] = timestamp
    if created_at is not None:
        raw['createdAt'] = created_at
    return ViCareEvent(raw)


def codes(events: list[ViCareEvent]) -> list[tuple[str | None, bool]]:
    return [(event.error_code, event.active) for event in events]


RAISE = error_event('F.380', True, '2026-11-26T01:17:32.000Z')
CLEAR = error_event('F.380', False, '2026-11-26T15:29:59.000Z')


class ChronologicalTest(unittest.TestCase):

    def test_oldest_first(self):
        # the API returns the newest first
        self.assertEqual(codes(chronological([CLEAR, RAISE])), [('F.380', True), ('F.380', False)])

    def test_equal_times_keep_the_order_they_happened_in(self):
        raised = error_event('F.380', True, '2026-11-26T01:17:32.000Z')
        cleared = error_event('F.380', False, '2026-11-26T01:17:32.000Z')
        self.assertEqual(codes(chronological([cleared, raised])), [('F.380', True), ('F.380', False)])

    def test_created_at_stands_in_for_a_missing_timestamp(self):
        late = error_event('F.357', True, None, created_at='2026-11-27T00:00:00.000Z')
        self.assertEqual(codes(chronological([late, RAISE])), [('F.380', True), ('F.357', True)])


class ViCareErrorHistoryTest(unittest.TestCase):

    def test_first_page_is_the_past(self):
        history = ViCareErrorHistory()
        self.assertFalse(history.initialized)
        page = readJson('response/events/device-error.json')
        events = [ViCareEvent(entry) for entry in page['data']]

        self.assertEqual(history.update(events), [])
        self.assertTrue(history.initialized)
        # the newest f4 is the clear
        self.assertEqual(history.active_errors('0'), [])

    def test_new_events_oldest_first(self):
        history = ViCareErrorHistory()
        history.update([CLEAR, RAISE])
        raised = error_event('F.357', True, '2026-11-27T08:00:00.000Z')
        cleared = error_event('F.357', False, '2026-11-27T08:05:00.000Z')

        new = history.update([cleared, raised, CLEAR, RAISE])

        self.assertEqual(codes(new), [('F.357', True), ('F.357', False)])
        self.assertEqual(history.update([cleared, raised, CLEAR, RAISE]), [])

    def test_active_errors(self):
        history = ViCareErrorHistory()
        standing = error_event('F.357', True, '2026-11-27T08:00:00.000Z')
        other_device = error_event('F.4', True, '2026-11-27T09:00:00.000Z', device_id='1')

        history.update([other_device, standing, CLEAR, RAISE])

        self.assertEqual(codes(history.active_errors('0')), [('F.357', True)])
        self.assertEqual(codes(history.active_errors('1')), [('F.4', True)])

    def test_standing_error_survives_dropping_off_the_page(self):
        history = ViCareErrorHistory()
        standing = error_event('F.357', True, '2026-11-20T08:00:00.000Z')
        history.update([standing])

        # newer events of another code push the raise off the page
        history.update([CLEAR, RAISE])

        self.assertEqual(codes(history.active_errors('0')), [('F.357', True)])

    def test_clear_ends_a_standing_error(self):
        history = ViCareErrorHistory()
        history.update([RAISE])
        history.update([CLEAR, RAISE])
        self.assertEqual(history.active_errors('0'), [])

    def test_events_without_device_or_code_are_ignored(self):
        history = ViCareErrorHistory()
        history.update([])
        nameless = ViCareEvent({'eventType': 'device-error', 'body': {'active': True}})
        self.assertEqual(history.update([nameless]), [])
        self.assertEqual(history.active_errors('0'), [])

    def test_restored_state_neither_repeats_nor_loses_events(self):
        history = ViCareErrorHistory()
        standing = error_event('F.357', True, '2026-11-20T08:00:00.000Z')
        history.update([standing, CLEAR, RAISE])

        # what a caller writes to storage and reads back
        restored = ViCareErrorHistory.from_dict(json.loads(json.dumps(history.as_dict())))

        self.assertTrue(restored.initialized)
        self.assertEqual(codes(restored.active_errors('0')), [('F.357', True)])
        # an error raised and cleared while the caller was stopped
        raised = error_event('F.4', True, '2026-11-28T08:00:00.000Z')
        cleared = error_event('F.4', False, '2026-11-28T08:01:00.000Z')
        self.assertEqual(
            codes(restored.update([cleared, raised, standing, CLEAR, RAISE])),
            [('F.4', True), ('F.4', False)])

    def test_restoring_unreadable_state_starts_over(self):
        for data in ({}, {'seen': 'garbage', 'standing': 3}, {'seen': [[1, 2]], 'standing': [None]}):
            with self.subTest(data=data):
                history = ViCareErrorHistory.from_dict(data)
                self.assertFalse(history.initialized)
                self.assertEqual(history.active_errors('0'), [])
