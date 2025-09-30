import unittest

from PyViCare.PyViCareGazBoiler import GazBoiler
from tests.helper import now_is
from tests.ViCareServiceMock import ViCareServiceMock


class Vitodens200W_B2HF(unittest.TestCase):
    def setUp(self):
        self.service = ViCareServiceMock('response/Vitodens200W_B2HF.json')
        self.device = GazBoiler(self.service)

    def test_getSupplyPressure(self):
        self.assertEqual(self.device.getSupplyPressure(), 1.5)

    def test_getSupplyPressureUnit(self):
        self.assertEqual(self.device.getSupplyPressureUnit(), 'bar')
