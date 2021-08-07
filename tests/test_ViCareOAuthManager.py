from PyViCare.PyViCareUtils import PyViCareRateLimitError, PyViCareCommandError
import unittest
from PyViCare.PyViCareOAuthManager import AbstractViCareOAuthManager
from unittest.mock import Mock
from tests.helper import readJson


class OAuthManagerWithMock(AbstractViCareOAuthManager):
    def __init__(self, mock):
        super().__init__(mock)

    def renewToken(self):
        self.oauth_session.renewToken()


class FakeResponse:
    def __init__(self, file_name):
        self.file_name = file_name

    def json(self):
        return readJson(self.file_name)


class PyViCareServiceTest(unittest.TestCase):

    def setUp(self):
        self.oauth_mock = Mock()
        self.manager = OAuthManagerWithMock(self.oauth_mock)

    def test_get_raiseratelimit_ifthatreponse(self):
        self.oauth_mock.get.return_value = FakeResponse(
            'response/rate_limit.json')

        def func():
            return self.manager.get("/")
        self.assertRaises(PyViCareRateLimitError, func)

    def test_post_raisecommanderror_ifthatreponse(self):
        self.oauth_mock.post.return_value = FakeResponse(
            'response/error_502.json')

        def func():
            return self.manager.post("/", {})
        self.assertRaises(PyViCareCommandError, func)

    def test_get_renewtoken_ifexpired(self):
        self.oauth_mock.get.side_effect = [
            FakeResponse('response/expired_token.json'),  # first call expired
            FakeResponse('response/Vitodens200W.json')  # second call success
        ]
        self.manager.get("/")
        self.oauth_mock.renewToken.assert_called_once()

    def test_post_raiseratelimit_ifthatreponse(self):
        self.oauth_mock.post.return_value = FakeResponse(
            'response/rate_limit.json')

        def func():
            return self.manager.post("/", "some")
        self.assertRaises(PyViCareRateLimitError, func)

    def test_post_renewtoken_ifexpired(self):
        self.oauth_mock.post.side_effect = [
            FakeResponse('response/expired_token.json'),  # first call expired
            FakeResponse('response/Vitodens200W.json')  # second call success
        ]
        self.manager.post("/", "some")
        self.oauth_mock.renewToken.assert_called_once()
