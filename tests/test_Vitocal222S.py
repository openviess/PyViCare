import datetime
from PyViCare.PyViCareUtils import ViCareTimer
import unittest

from PyViCare.PyViCareHeatPump import HeatPump
from tests.ViCareServiceMock import ViCareServiceMock
from unittest.mock import patch


class Vitocal222S(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitocal222S.json')
        self.device = HeatPump(self.service)

    def test_getDomesticHotWaterActiveMode_10_10_time(self):
        with patch.object(ViCareTimer, 'now', return_value=datetime.datetime(2000, 1, 1, 10, 10, 0)):
            self.assertEqual(
                self.device.getDomesticHotWaterActiveMode(), 'normal')
