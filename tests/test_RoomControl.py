import unittest

from PyViCare.PyViCareRoomControl import RoomControl
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.ViCareServiceMock import ViCareServiceMock


class TestRoomControl(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/RoomControl.json')
        self.device = RoomControl(self.service)

    def test_rooms(self):
        self.assertGreater(len(self.device.rooms), 0)

    def test_room_getType(self):
        self.assertEqual(self.device.rooms[0].getType(), "livingroom")

    def test_room_getName(self):
        self.assertEqual(self.device.rooms[0].getName(), "Living room")

    def test_room_actors(self):
        self.assertGreater(len(self.device.rooms[0].actors), 0)

    def test_room_getSensorTemperature(self):
        self.assertEqual(self.device.rooms[0].getSensorTemperature(), 25.4)

    def test_room_getSensorTemperatureStatus(self):
        self.assertEqual(self.device.rooms[0].getSensorTemperatureStatus(), "connected")

    def test_room_getSensorHumidity(self):
        self.assertEqual(self.device.rooms[0].getSensorHumidity(), 60)

    def test_room_getSensorHumidityStatus(self):
        self.assertEqual(self.device.rooms[0].getSensorHumidityStatus(), "connected")

    def test_room_getSensorCO2(self):
        def func():
            return self.device.rooms[0].getSensorCO2()

        self.assertRaises(PyViCareNotSupportedFeatureError, func)

    def test_room_getSensorCO2Status(self):
        self.assertEqual(self.device.rooms[0].getSensorCO2Status(), "notConnected")

    def test_room_getOperatingStateLevel(self):
        self.assertEqual(self.device.rooms[0].getOperatingStateLevel(), "normal")

    def test_room_getOperatingStateDemand(self):
        self.assertEqual(self.device.rooms[0].getOperatingStateDemand(), "cooling")

    def test_room_getOperatingStateReason(self):
        self.assertEqual(self.device.rooms[0].getOperatingStateReason(), "schedule")

    def test_room_getOperatingStateModifier(self):
        self.assertEqual(self.device.rooms[0].getOperatingStateModifier(), "none")

    def test_room_getNormalHeatingTemperature(self):
        self.assertEqual(self.device.rooms[0].getNormalHeatingTemperature(), 22)

    def test_room_getNormalHeatingActive(self):
        self.assertEqual(self.device.rooms[0].getNormalHeatingActive(), False)

    def test_room_setNormalHeatingTemperature(self):
        self.device.rooms[0].setNormalHeatingTemperature(22)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'setTemperature')
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'rooms.0.operating.programs.normalHeating')
        self.assertEqual(
            self.service.setPropertyData[0]['data'], {'targetTemperature': 22})

    def test_room_getReducedHeatingTemperature(self):
        self.assertEqual(self.device.rooms[0].getReducedHeatingTemperature(), 22)

    def test_room_getReducedHeatingActive(self):
        self.assertEqual(self.device.rooms[0].getReducedHeatingActive(), False)

    def test_room_setReducedHeatingTemperature(self):
        self.device.rooms[0].setReducedHeatingTemperature(22)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'setTemperature')
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'rooms.0.operating.programs.reducedHeating')
        self.assertEqual(
            self.service.setPropertyData[0]['data'], {'targetTemperature': 22})

    def test_room_getComfortHeatingTemperature(self):
        self.assertEqual(self.device.rooms[0].getComfortHeatingTemperature(), 22)

    def test_room_getComfortHeatingActive(self):
        self.assertEqual(self.device.rooms[0].getComfortHeatingActive(), False)

    def test_room_setComfortHeatingTemperature(self):
        self.device.rooms[0].setComfortHeatingTemperature(22)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'setTemperature')
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'rooms.0.operating.programs.comfortHeating')
        self.assertEqual(
            self.service.setPropertyData[0]['data'], {'targetTemperature': 22})

    def test_room_getNormalCoolingTemperature(self):
        self.assertEqual(self.device.rooms[0].getNormalCoolingTemperature(), 23)

    def test_room_getNormalCoolingActive(self):
        self.assertEqual(self.device.rooms[0].getNormalCoolingActive(), True)

    def test_room_setNormalCoolingTemperature(self):
        self.device.rooms[0].setNormalCoolingTemperature(22)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'setTemperature')
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'rooms.0.operating.programs.normalCooling')
        self.assertEqual(
            self.service.setPropertyData[0]['data'], {'targetTemperature': 22})

    def test_room_getReducedCoolingTemperature(self):
        self.assertEqual(self.device.rooms[0].getReducedCoolingTemperature(), 27)

    def test_room_getReducedCoolingActive(self):
        self.assertEqual(self.device.rooms[0].getReducedCoolingActive(), False)

    def test_room_setReducedCoolingTemperature(self):
        self.device.rooms[0].setReducedCoolingTemperature(22)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'setTemperature')
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'rooms.0.operating.programs.reducedCooling')
        self.assertEqual(
            self.service.setPropertyData[0]['data'], {'targetTemperature': 22})

    def test_room_getComfortCoolingTemperature(self):
        self.assertEqual(self.device.rooms[0].getComfortCoolingTemperature(), 23)

    def test_room_getComfortCoolingActive(self):
        self.assertEqual(self.device.rooms[0].getComfortCoolingActive(), False)

    def test_room_setComfortCoolingTemperature(self):
        self.device.rooms[0].setComfortCoolingTemperature(22)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'setTemperature')
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'rooms.0.operating.programs.comfortCooling')
        self.assertEqual(
            self.service.setPropertyData[0]['data'], {'targetTemperature': 22})

    def test_room_getSchedule(self):
        self.assertEqual(self.device.rooms[0].getSchedule(), {
            'active': True,
            'mon': [
                {
                    "end": "22:00",
                    "mode": "normal",
                    "start": "06:00",
                    "position": 0
                }],
            "tue": [
                {
                    "mode": "normal",
                    "start": "06:00",
                    "end": "22:00",
                    "position": 0
                }
            ],
            "wed": [
                {
                    "mode": "normal",
                    "start": "06:00",
                    "end": "22:00",
                    "position": 0
                }
            ],
            "thu": [
                {
                    "mode": "normal",
                    "start": "06:00",
                    "end": "22:00",
                    "position": 0
                }
            ],
            "fri": [
                {
                    "mode": "normal",
                    "start": "06:00",
                    "end": "22:00",
                    "position": 0
                }
            ],
            "sat": [
                {
                    "mode": "normal",
                    "start": "06:00",
                    "end": "22:00",
                    "position": 0
                }
            ],
            "sun": [
                {
                    "mode": "normal",
                    "start": "06:00",
                    "end": "22:00",
                    "position": 0
                }
            ]
        })

    def test_room_getManualTillNextScheduleActive(self):
        self.assertEqual(self.device.rooms[0].getManualTillNextScheduleActive(), False)

    def test_room_setManualTillNextScheduleTemperature(self):
        self.device.rooms[0].setManualTillNextScheduleTemperature(22)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'setTemperature')
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'rooms.0.quickmodes.manualTillNextSchedule')
        self.assertEqual(
            self.service.setPropertyData[0]['data'], {'targetTemperature': 22})

    def test_room_activateManualTillNextSchedule(self):
        self.device.rooms[0].activateManualTillNextSchedule(22)
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'activate')
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'rooms.0.quickmodes.manualTillNextSchedule')
        self.assertEqual(
            self.service.setPropertyData[0]['data'], {'temperature': 22})

    def test_room_deactivateManualTillNextSchedule(self):
        self.device.rooms[0].deactivateManualTillNextSchedule()
        self.assertEqual(len(self.service.setPropertyData), 1)
        self.assertEqual(self.service.setPropertyData[0]['action'], 'deactivate')
        self.assertEqual(
            self.service.setPropertyData[0]['property_name'], 'rooms.0.quickmodes.manualTillNextSchedule')
        self.assertEqual(
            self.service.setPropertyData[0]['data'], {})
