import datetime
import unittest
from unittest.mock import patch

from PyViCare.PyViCareHeatPump import HeatPump
from PyViCare.PyViCareUtils import ViCareTimer
from tests.ViCareServiceMock import ViCareServiceMock


class Vitocal222S(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal222S.json')
        self.device = HeatPump(self.service)

    def test_getDomesticHotWaterActiveMode_10_10_time(self):
        with patch.object(ViCareTimer, 'now', return_value=datetime.datetime(2000, 1, 1, 10, 10, 0)):
            self.assertEqual(
                self.device.getDomesticHotWaterActiveMode(), 'normal')
