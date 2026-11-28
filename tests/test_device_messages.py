import unittest

from PyViCare.PyViCareDevice import Device
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.helper import readJson
from tests.ViCareServiceMock import ViCareServiceMock


class ReportsDeviceMessagesTest(unittest.TestCase):

    def device(self, filename, device_id="0"):
        accessor = ViCareDeviceAccessor("[id]", "[serial]", device_id)
        return Device(accessor, ViCareServiceMock(filename))

    def test_error_messages(self):
        self.assertTrue(self.device('response/Vitodens100NA.json').reportsDeviceMessages())

    def test_logbook_only(self):
        # older heat pumps report a logbook instead of the raw messages
        self.assertTrue(self.device('response/Vitocal200S_AWB-M-E-AC-201.D10.json').reportsDeviceMessages())

    def test_no_messages(self):
        self.assertFalse(self.device('response/RoomControl.json').reportsDeviceMessages())

    def test_messages_of_another_device_on_the_gateway(self):
        # a gateway payload holds the features of every device behind it
        self.assertFalse(self.device('response/Vitodens100NA.json', device_id="1").reportsDeviceMessages())

    def test_features_not_paid_for(self):
        accessor = ViCareDeviceAccessor("[id]", "[serial]", "0")
        service = ViCareServiceMock(None, rawInput=readJson('response/Vitodens100NA.json'))

        def not_paid_for(_accessor):
            raise PyViCareNotSupportedFeatureError("PACKAGE_NOT_PAID_FOR")

        service.fetch_all_features = not_paid_for
        self.assertFalse(Device(accessor, service).reportsDeviceMessages())
