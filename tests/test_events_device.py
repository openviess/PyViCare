import unittest
from typing import Any, ClassVar
from unittest.mock import Mock

from PyViCare.PyViCare import PyViCare
from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareEvent import ViCareEventPage
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareServiceViaGateway import ViCareServiceViaGateway
from tests.helper import readJson


class DeviceEventsTest(unittest.TestCase):

    def setUp(self):
        self.service = Mock()
        self.service.fetch_events.return_value = ViCareEventPage.from_payload(
            readJson('response/events/device-error-multi-device.json'))
        self.accessor = ViCareDeviceAccessor('[id]', '[serial]', '0')
        self.device = Device(self.accessor, self.service)

    def test_getEvents_filters_by_device(self):
        events = self.device.getEvents()
        self.assertEqual([event.error_code for event in events], ['fb'])

    def test_getEvents_forwards_query(self):
        self.device.getEvents('device-error', limit=5, cursor='abc')
        self.service.fetch_events.assert_called_once_with(
            self.accessor, 'device-error', None, None, None, 5, 'abc')

    def test_getErrorEvents_sets_event_type(self):
        self.device.getErrorEvents(limit=3)
        self.service.fetch_events.assert_called_once_with(
            self.accessor, 'device-error', None, None, None, 3, None)

    def test_getErrorEvents_forwards_window(self):
        self.device.getErrorEvents(last_days=7)
        self.service.fetch_events.assert_called_once_with(
            self.accessor, 'device-error', 7, None, None, 10, None)

    def test_getEventPage_is_not_filtered(self):
        page = self.device.getEventPage()
        self.assertEqual({event.device_id for event in page.events}, {'0', 'gateway'})
        self.assertIsNotNone(page.next_cursor)

    def test_gateway_device_sees_its_own_events(self):
        gateway = Device(ViCareDeviceAccessor('[id]', '[serial]', 'gateway'), self.service)
        events = gateway.getEvents()
        self.assertEqual([event.error_code for event in events], ['A9'])

    def test_devices_without_events_get_an_empty_list(self):
        other = Device(ViCareDeviceAccessor('[id]', '[serial]', '1'), self.service)
        self.assertEqual(other.getEvents(), [])


class DeviceConfigEventsTest(unittest.TestCase):

    def setUp(self):
        self.service = Mock()
        self.service.fetch_events.return_value = ViCareEventPage.from_payload(
            readJson('response/events/device-error-multi-device.json'))
        self.config = PyViCareDeviceConfig(
            ViCareDeviceAccessor('[id]', '[serial]', '0'), self.service, 'VPlusHO1_4', 'Online')

    def test_getEvents_filters_by_device(self):
        events = self.config.getEvents()
        self.assertEqual([event.error_code for event in events], ['fb'])

    def test_getErrorEvents_sets_event_type(self):
        self.config.getErrorEvents(limit=2)
        self.service.fetch_events.assert_called_once_with(
            self.config.accessor, 'device-error', None, None, None, 2, None)

    def test_getEventPage_is_not_filtered(self):
        page = self.config.getEventPage()
        self.assertEqual(len(page.events), 2)


class GatewayModeEventsTest(unittest.TestCase):
    """All devices of a gateway share one service, so one events fetch."""

    INSTALLATION: ClassVar[dict[str, Any]] = {
        "data": [{
            "id": 1234567,
            "gateways": [{
                "serial": "[serial]",
                "devices": [
                    {"id": "gateway", "modelId": "Heatbox1", "status": "Online",
                     "deviceType": "vitoconnect", "roles": ["type:gateway;VitoconnectOpto1"]},
                    {"id": "0", "modelId": "VPlusHO1_4", "status": "Online",
                     "deviceType": "heating", "roles": ["type:boiler"]},
                ],
            }],
        }]
    }

    def test_one_events_fetch_for_all_devices(self):
        events_payload = readJson('response/events/device-error-multi-device.json')
        bulk_payload = {"data": []}
        oauth = Mock()
        oauth.get.side_effect = lambda url: (
            self.INSTALLATION if url.startswith('/equipment/installations')
            else events_payload if url.startswith('/events-history/')
            else bulk_payload)

        vicare = PyViCare()
        vicare.loadViaGateway(True)
        vicare.initWithExternalOAuth(oauth)

        pages = [device.getEventPage() for device in vicare.devices]
        self.assertTrue(all(isinstance(page, ViCareEventPage) for page in pages))
        event_calls = [c for c in oauth.get.call_args_list
                       if c.args[0].startswith('/events-history/')]
        self.assertEqual(len(event_calls), 1)

    def test_service_is_shared_and_url_is_installation_scoped(self):
        oauth = Mock()
        oauth.get.side_effect = lambda url: (
            self.INSTALLATION if url.startswith('/equipment/installations')
            else readJson('response/events/device-error-multi-device.json'))
        vicare = PyViCare()
        vicare.loadViaGateway(True)
        vicare.initWithExternalOAuth(oauth)

        self.assertIsInstance(vicare.devices[0].service, ViCareServiceViaGateway)
        vicare.devices[-1].getEventPage()
        event_urls = [c.args[0] for c in oauth.get.call_args_list
                      if c.args[0].startswith('/events-history/')]
        self.assertEqual(event_urls, ['/events-history/installations/1234567/events?limit=10'])
