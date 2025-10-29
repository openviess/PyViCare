import unittest

from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class DeviceErrorTest(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/deviceerrors/F.1100.json')
        self.device = Device(self.accessor, self.service)

    def test_deviceErrors(self):
        errors = self.device.getDeviceErrors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["errorCode"], "F.1100")
        self.assertEqual(errors[0]["priority"], "criticalError")
