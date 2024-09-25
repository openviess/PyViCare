import unittest
from unittest.mock import Mock

from PyViCare.PyViCareCachedService import ViCareCachedService
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.helper import now_is


class PyViCareCachedServiceTest(unittest.TestCase):

    CACHE_DURATION = 60

    def setUp(self):
        self.oauth_mock = Mock()
        self.oauth_mock.get.return_value = {'data': [{"feature": "someprop"}]}
        accessor = ViCareDeviceAccessor("[id]", "[serial]", "[device]")
        self.service = ViCareCachedService(
            self.oauth_mock, accessor, [], self.CACHE_DURATION)

    def test_getProperty_existing(self):
        self.service.getProperty("someprop")
        self.oauth_mock.get.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/devices/[device]/features/')

    def test_getProperty_nonexisting_raises_exception(self):

        def func():
            return self.service.getProperty("some-non-prop")
        self.assertRaises(PyViCareNotSupportedFeatureError, func)

    def test_setProperty_works(self):
        self.service.setProperty("someotherprop", "doaction", {'name': 'abc'})
        self.oauth_mock.post.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/devices/[device]/features/someotherprop/commands/doaction', '{"name": "abc"}')

    def test_getProperty_existing_cached(self):
        # time+0 seconds
        with now_is('2000-01-01 00:00:00'):
            self.service.getProperty("someprop")
            self.service.getProperty("someprop")

        # time+30 seconds
        with now_is('2000-01-01 00:00:30'):
            self.service.getProperty("someprop")

        self.assertEqual(self.oauth_mock.get.call_count, 1)
        self.oauth_mock.get.assert_called_once_with(
            '/features/installations/[id]/gateways/[serial]/devices/[device]/features/')

        # time+70 seconds (must be more than CACHE_DURATION)
        with now_is('2000-01-01 00:01:10'):
            self.service.getProperty("someprop")

        self.assertEqual(self.oauth_mock.get.call_count, 2)

    def test_setProperty_invalidateCache(self):
        # freeze time
        with now_is('2000-01-01 00:00:00'):
            self.assertEqual(self.service.is_cache_invalid(), True)
            self.service.getProperty("someprop")
            self.assertEqual(self.service.is_cache_invalid(), False)

            self.service.setProperty(
                "someotherprop", "doaction", {'name': 'abc'})
            self.assertEqual(self.service.is_cache_invalid(), True)

            self.service.getProperty("someprop")
            self.assertEqual(self.oauth_mock.get.call_count, 2)
