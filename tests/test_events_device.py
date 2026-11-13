import unittest
from datetime import UTC, date, datetime
from typing import Any, ClassVar
from unittest.mock import Mock

from PyViCare.PyViCare import PyViCare
from PyViCare.PyViCareDevice import Device
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

    def test_gateway_device_events(self):
        gateway = Device(ViCareDeviceAccessor('[id]', '[serial]', 'gateway'), self.service)
        events = gateway.getErrorEvents()
        self.assertEqual([event.error_code for event in events], ['A9'])

    def test_unknown_device_is_empty(self):
        other = Device(ViCareDeviceAccessor('[id]', '[serial]', '1'), self.service)
        self.assertEqual(other.getErrorEvents(), [])

    def test_requests_its_gateway_and_device_error_type(self):
        self.device.getErrorEvents()
        self.service.fetch_events.assert_called_once_with(
            self.accessor, 'device-error',
            last_days=None, since=None, on_date=None,
            gateway_serials='[serial]', limit=10)

    def test_forwards_window_and_limit(self):
        self.device.getErrorEvents(last_days=7, limit=5)
        self.service.fetch_events.assert_called_once_with(
            self.accessor, 'device-error',
            last_days=7, since=None, on_date=None,
            gateway_serials='[serial]', limit=5)

    def test_forwards_since(self):
        moment = datetime(2026, 10, 1, tzinfo=UTC)
        self.device.getErrorEvents(since=moment)
        self.service.fetch_events.assert_called_once_with(
            self.accessor, 'device-error',
            last_days=None, since=moment, on_date=None,
            gateway_serials='[serial]', limit=10)

    def test_forwards_on_date(self):
        self.device.getErrorEvents(on_date=date(2026, 10, 17))
        self.service.fetch_events.assert_called_once_with(
            self.accessor, 'device-error',
            last_days=None, since=None, on_date=date(2026, 10, 17),
            gateway_serials='[serial]', limit=10)


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
        page = device.service.fetch_events(
            device.accessor, 'device-error', gateway_serials='[serial]', limit=2)
        self.assertEqual(len(page.events), 2)
        self.assertEqual(
            self._event_urls(),
            [('/events-history/installations/1234567/events'
              '?eventType=device-error&gatewaySerials=%5Bserial%5D&limit=2')])

    def test_get_error_events_costs_one_request_per_call(self):
        # no event cache: a consumer that wants every device should call
        # fetch_events() once and filter itself
        for config in self.vicare.devices:
            config.asAutoDetectDevice().getErrorEvents()

        self.assertEqual(len(self._event_urls()), len(self.vicare.devices))

    def test_get_error_events_sends_the_gateway(self):
        self.vicare.devices[-1].asAutoDetectDevice().getErrorEvents()
        self.assertIn('gatewaySerials=%5Bserial%5D', self._event_urls()[0])
