import unittest

from PyViCare.PyViCareDevice import Device
from tests.ViCareServiceMock import ViCareServiceMock


class DeviceErrorTest(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/deviceerrors/F.1100.json')
        self.device = Device(self.service)

    def test_deviceErrors(self):
        errors = self.device.getDeviceErrors()
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["errorCode"], "F.1100")
        self.assertEqual(errors[0]["priority"], "criticalError")
