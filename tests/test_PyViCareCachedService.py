import unittest
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareCachedService import ViCareCachedService, ViCareTimer
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from unittest.mock import Mock, patch
import datetime

class PyViCareCachedServiceTest(unittest.TestCase):

    CACHE_DURATION = 60

    def setUp(self):
        self.oauth_mock = Mock()
        self.oauth_mock.get.return_value = {'data' : [{"feature": "someprop"}]}
        accessor = ViCareDeviceAccessor("[id]", "[serial]", "[device]")
        self.service = ViCareCachedService(self.oauth_mock, accessor, self.CACHE_DURATION)
        
    def test_getProperty_existing(self):
        self.service.getProperty("someprop")
        self.oauth_mock.get.assert_called_once_with('/equipment/installations/[id]/gateways/[serial]/devices/[device]/features/')

    def test_getProperty_nonexisting_raises_exception(self):
        func = lambda: self.service.getProperty("some-non-prop")
        self.assertRaises(PyViCareNotSupportedFeatureError, func)

    def test_getProperty_existing_cached(self):
        #time 0 seconds
        with patch.object(ViCareTimer, 'now', return_value=datetime.datetime(2000, 1, 1, 0, 0, 0)):
            self.service.getProperty("someprop")

        #time 30 seconds
        with patch.object(ViCareTimer, 'now', return_value=datetime.datetime(2000, 1, 1, 0, 0, 30)):
            self.service.getProperty("someprop")

        self.oauth_mock.get.assert_called_once_with('/equipment/installations/[id]/gateways/[serial]/devices/[device]/features/')

        self.oauth_mock.reset_mock()
        
        #time 70 seconds (more than CACHE_DURATION)
        with patch.object(ViCareTimer, 'now', return_value=datetime.datetime(2000, 1, 1, 0, 1, 10)):
            self.service.getProperty("someprop")

        self.oauth_mock.get.assert_called_once_with('/equipment/installations/[id]/gateways/[serial]/devices/[device]/features/')

    def test_setProperty_invalidateCache(self):
        self.service.cache = 'exists'
        self.service.setProperty("someprop", "doaction", {'name': 'abc'})
        self.oauth_mock.post.assert_called_once_with('/equipment/installations/[id]/gateways/[serial]/devices/[device]/features/someprop/doaction', '{"name": "abc"}')
        self.assertIsNone(self.service.cache)