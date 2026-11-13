import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from PyViCare.PyViCareService import ViCareDeviceAccessor
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens300W_B3HF(unittest.TestCase):
    def setUp(self):
        self.accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        self.service = ViCareServiceMock('response/Vitodens300W_B3HF-19.json')
        self.device = GazBoiler(self.accessor, self.service)

    def test_getHydraulicSeparatorTemperature(self):
        self.assertEqual(self.device.getHydraulicSeparatorTemperature(), 25.7)
