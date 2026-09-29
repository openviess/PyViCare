"""PyViCare.devices exposes only known device types."""
import unittest
from unittest.mock import Mock

from PyViCare.PyViCare import PyViCare

INSTALLATIONS_OBNG = {
    "data": [{
        "id": 1234567,
        "description": "Test Installation",
        "address": {"street": "Teststreet"},
        "gateways": [{
            "serial": "1234567812345678",
            "producedAt": "2024-01-01T00:00:00.000Z",
            "autoUpdate": True,
            "aggregatedStatus": "Online",
            "registeredAt": "2024-01-01T00:00:00.000Z",
            "devices": [
                {"id": "0", "modelId": "OBNG_SCU_01", "status": "Online",
                 "deviceType": "systemController",
                 "roles": ["type:OBNG", "type:product;SystemController"],
                 "createdAt": "2024-01-01T00:00:00.000Z"},
                {"id": "1", "modelId": "OBNG_OCU", "status": "Online",
                 "deviceType": "outdoorUnit",
                 "roles": ["type:OBNG", "type:product;OutdoorUnitMonoAir"],
                 "createdAt": "2024-01-01T00:00:00.000Z"},
                {"id": "2", "modelId": "OBNG_HIOU", "status": "Online",
                 "deviceType": "indoorUnit",
                 "roles": ["type:OBNG", "type:product;IndoorUnitMonoStandard"],
                 "createdAt": "2024-01-01T00:00:00.000Z"},
                {"id": "RoomControl-1", "modelId": "OBNG_RoomControl_One_01",
                 "status": "Online", "deviceType": "roomControl",
                 "roles": ["type:OBNG", "type:virtual;smartRoomControl"],
                 "createdAt": "2024-01-01T00:00:00.000Z"},
            ],
        }],
    }]
}


class DeviceTypeFilterTest(unittest.TestCase):

    def setUp(self):
        oauth = Mock()
        oauth.get.return_value = INSTALLATIONS_OBNG
        self.vicare = PyViCare()
        self.vicare.initWithExternalOAuth(oauth)

    def models(self):
        return [d.getModel() for d in self.vicare.devices]

    def test_system_controller_is_kept(self):
        self.assertIn("OBNG_SCU_01", self.models())

    def test_outdoor_unit_is_kept(self):
        self.assertIn("OBNG_OCU", self.models())

    def test_indoor_unit_is_dropped(self):
        self.assertNotIn("OBNG_HIOU", self.models())

    def test_all_devices_is_unfiltered(self):
        self.assertEqual(len(self.vicare.all_devices), 4)
