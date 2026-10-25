import unittest
from datetime import UTC, datetime
from typing import Any, ClassVar
from unittest.mock import Mock

from PyViCare.PyViCare import PyViCare
from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareDeviceConfig import PyViCareDeviceConfig
from PyViCare.PyViCareEvent import ViCareEventPage
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.helper import readJson


class DeviceErrorEventsTest(unittest.TestCase):

    def setUp(self):
        self.service = Mock()
        self.service.fetch_events.return_value = ViCareEventPage.from_payload(
            readJson('response/events/device-error-multi-device.json'))
        self.accessor = ViCareDeviceAccessor('[id]', '[serial]', '0')
        self.device = Device(self.accessor, self.service)

    def test_filters_by_device(self):
        events = self.device.getErrorEvents()
        self.assertEqual([event.error_code for event in events], ['fb'])

    def test_same_device_id_on_another_gateway_is_excluded(self):
        other = Device(ViCareDeviceAccessor('[id]', '[other-serial]', '0'), self.service)
        events = other.getErrorEvents()
        self.assertEqual([event.error_code for event in events], ['f4'])

    def test_gateway_device_events(self):
        gateway = Device(ViCareDeviceAccessor('[id]', '[serial]', 'gateway'), self.service)
        events = gateway.getErrorEvents()
        self.assertEqual([event.error_code for event in events], ['A9'])

    def test_unknown_device_is_empty(self):
        other = Device(ViCareDeviceAccessor('[id]', '[serial]', '1'), self.service)
        self.assertEqual(other.getErrorEvents(), [])

    def test_requests_device_error_type(self):
        self.device.getErrorEvents()
        self.service.fetch_events.assert_called_once_with(
            self.accessor, 'device-error', None, None, None, 10)

    def test_forwards_window_and_limit(self):
        self.device.getErrorEvents(last_days=7, limit=5)
        self.service.fetch_events.assert_called_once_with(
            self.accessor, 'device-error', 7, None, None, 5)

    def test_forwards_since(self):
        moment = datetime(2026, 10, 1, tzinfo=UTC)
        self.device.getErrorEvents(since=moment)
        self.service.fetch_events.assert_called_once_with(
            self.accessor, 'device-error', None, moment, None, 10)


class DeviceConfigErrorEventsTest(unittest.TestCase):

    def setUp(self):
        self.service = Mock()
        self.service.fetch_events.return_value = ViCareEventPage.from_payload(
            readJson('response/events/device-error-multi-device.json'))
        self.accessor = ViCareDeviceAccessor('[id]', '[serial]', '0')
        self.config = PyViCareDeviceConfig(self.accessor, self.service, 'VPlusHO1_4', 'Online')

    def test_filters_by_device_and_gateway(self):
        events = self.config.getErrorEvents()
        self.assertEqual([event.error_code for event in events], ['fb'])

    def test_same_device_id_on_another_gateway_is_excluded(self):
        config = PyViCareDeviceConfig(
            ViCareDeviceAccessor('[id]', '[other-serial]', '0'), self.service, 'VITOCAL_250_A', 'Online')
        events = config.getErrorEvents()
        self.assertEqual([event.error_code for event in events], ['f4'])

    def test_requests_device_error_type(self):
        self.config.getErrorEvents(limit=2)
        self.service.fetch_events.assert_called_once_with(
            self.accessor, 'device-error', None, None, None, 2)


class GatewayModeEventsTest(unittest.TestCase):
    """In gateway mode one service serves all devices, but events are uncached."""

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

    def setUp(self):
        self.events_payload = readJson('response/events/device-error-multi-device.json')
        self.oauth = Mock()
        self.oauth.get.side_effect = lambda url: (
            self.INSTALLATION if url.startswith('/equipment/installations')
            else self.events_payload)
        self.vicare = PyViCare()
        self.vicare.loadViaGateway(True)
        self.vicare.initWithExternalOAuth(self.oauth)

    def _event_urls(self) -> list[str]:
        return [call.args[0] for call in self.oauth.get.call_args_list
                if call.args[0].startswith('/events-history/')]

    def test_fetch_events_is_installation_scoped(self):
        device = self.vicare.devices[0]
        page = device.service.fetch_events(device.accessor, 'device-error', limit=2)
        self.assertEqual(len(page.events), 3)
        self.assertEqual(
            self._event_urls(),
            ['/events-history/installations/1234567/events?eventType=device-error&limit=2'])

    def test_get_error_events_costs_one_request_per_call(self):
        # no event cache: a consumer that wants every device should call
        # fetch_events() once and filter itself
        for device in self.vicare.devices:
            device.getErrorEvents()

        self.assertEqual(len(self._event_urls()), len(self.vicare.devices))
