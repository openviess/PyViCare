import unittest
from unittest.mock import Mock, patch

import pytest
import requests
from authlib.integrations.base_client.errors import OAuthError

from PyViCare.PyViCareOAuthManager import (AbstractViCareOAuthManager,
                                           obtain_token_via_basic_auth_pkce)
from PyViCare.PyViCareUtils import (PyViCareCommandError,
                                    PyViCareDeviceCommunicationError,
                                    PyViCareInternalServerError,
                                    PyViCareRateLimitError)
from tests.helper import readJson


class OAuthManagerWithMock(AbstractViCareOAuthManager):
    def __init__(self, mock):
        super().__init__(mock)

    def renewToken(self):
        self.oauth_session.renewToken()


class FakeResponse:
    def __init__(self, file_name, status_code=200, content_type='application/json'):
        self.file_name = file_name
        self.status_code = status_code
        self.headers = {'content-type': content_type}

    def json(self):
        return readJson(self.file_name)


class PyViCareServiceTest(unittest.TestCase):

    def setUp(self):
        self.oauth_mock = Mock()
        self.manager = OAuthManagerWithMock(self.oauth_mock)

    def test_get_raiseratelimit_ifthatreponse(self):
        self.oauth_mock.get.return_value = FakeResponse(
            'response/errors/rate_limit.json')

        def func():
            return self.manager.get("/")
        self.assertRaises(PyViCareRateLimitError, func)

    def test_post_raisecommanderror_ifthatreponse(self):
        self.oauth_mock.post.return_value = FakeResponse(
            'response/errors/error_502.json')

        def func():
            return self.manager.post("/", {})
        self.assertRaises(PyViCareCommandError, func)

    def test_get_raiseservererror_ifthatreponse(self):
        self.oauth_mock.get.return_value = FakeResponse(
            'response/errors/error_500.json')

        def func():
            return self.manager.get("/")
        self.assertRaises(PyViCareInternalServerError, func)

    def test_get_raisedevicecommunicationerror_gateway_offline(self):
        self.oauth_mock.get.return_value = FakeResponse(
            'response/errors/gateway_offline.json')

        def func():
            return self.manager.get("/")
        self.assertRaises(PyViCareDeviceCommunicationError, func)

    def test_get_raisedevicecommunicationerror_device_offline(self):
        self.oauth_mock.get.return_value = FakeResponse(
            'response/errors/device_offline.json')

        def func():
            return self.manager.get("/")
        self.assertRaises(PyViCareDeviceCommunicationError, func)

    def test_get_renewtoken_ifexpired(self):
        self.oauth_mock.get.side_effect = [
            FakeResponse('response/errors/expired_token.json'),  # first call expired
            FakeResponse('response/Vitodens200W.json')  # second call success
        ]
        self.manager.get("/")
        self.oauth_mock.renewToken.assert_called_once()

    def test_post_raiseratelimit_ifthatreponse(self):
        self.oauth_mock.post.return_value = FakeResponse(
            'response/errors/rate_limit.json')

        def func():
            return self.manager.post("/", "some")
        self.assertRaises(PyViCareRateLimitError, func)

    def test_get_raise_on_non_json_502(self):
        response = Mock()
        response.status_code = 502
        response.headers = {'content-type': 'text/html'}
        self.oauth_mock.get.return_value = response

        def func():
            return self.manager.get("/")
        self.assertRaises(PyViCareInternalServerError, func)

    def test_get_raise_on_extended_payload_timeout(self):
        self.oauth_mock.get.return_value = FakeResponse.__new__(FakeResponse)
        self.oauth_mock.get.return_value.status_code = 200
        self.oauth_mock.get.return_value.headers = {'content-type': 'application/json'}
        self.oauth_mock.get.return_value.json = lambda: {
            'viErrorId': '00-abc-def-00',
            'errorType': '',
            'message': '',
            'extendedPayload': {'code': '500', 'reason': 'TIMEOUT'}
        }

        def func():
            return self.manager.get("/")
        self.assertRaises(PyViCareInternalServerError, func)

    def test_get_raise_on_connection_error(self):
        self.oauth_mock.get.side_effect = OSError("Timeout while contacting DNS servers")

        def func():
            return self.manager.get("/")
        self.assertRaises(PyViCareInternalServerError, func)

    def test_post_raise_on_connection_error(self):
        self.oauth_mock.post.side_effect = OSError("Connection refused")

        def func():
            return self.manager.post("/", {})
        self.assertRaises(PyViCareInternalServerError, func)

    def test_post_raise_on_non_json_502(self):
        response = Mock()
        response.status_code = 502
        response.headers = {'content-type': 'text/html'}
        self.oauth_mock.post.return_value = response

        def func():
            return self.manager.post("/", {})
        self.assertRaises(PyViCareInternalServerError, func)

    def test_post_renewtoken_ifexpired(self):
        self.oauth_mock.post.side_effect = [
            FakeResponse('response/errors/expired_token.json'),  # first call expired
            FakeResponse('response/Vitodens200W.json')  # second call success
        ]
        self.manager.post("/", "some")
        self.oauth_mock.renewToken.assert_called_once()


@pytest.mark.filterwarnings(
    "ignore:obtain_token_via_basic_auth_pkce:DeprecationWarning"
)
class ObtainTokenViaBasicAuthPkceTest(unittest.TestCase):

    @patch('PyViCare.PyViCareOAuthManager.OAuth2Session')
    @patch('PyViCare.PyViCareOAuthManager.requests.post')
    def test_returns_token_on_success(self, mock_post, mock_oauth_cls):
        mock_oauth = Mock()
        mock_oauth.create_authorization_url.return_value = ('http://auth', 'state')
        mock_oauth.token = {'access_token': 'a', 'refresh_token': 'r'}
        mock_oauth_cls.return_value = mock_oauth

        mock_post.return_value = Mock(
            status_code=302,
            headers={'Location': 'vicare://oauth-callback/everest?code=xyz'},
        )

        token = obtain_token_via_basic_auth_pkce('client', 'user', 'pass')
        self.assertEqual(token, {'access_token': 'a', 'refresh_token': 'r'})
        mock_oauth.fetch_token.assert_called_once()

    @patch('PyViCare.PyViCareOAuthManager.requests.post')
    def test_returns_empty_on_request_exception(self, mock_post):
        mock_post.side_effect = requests.RequestException("network down")
        self.assertEqual(
            obtain_token_via_basic_auth_pkce('client', 'user', 'pass'), {})

    @patch('PyViCare.PyViCareOAuthManager.OAuth2Session')
    @patch('PyViCare.PyViCareOAuthManager.requests.post')
    def test_returns_empty_on_non_redirect_response(self, mock_post, mock_oauth_cls):
        mock_oauth_cls.return_value.create_authorization_url.return_value = (
            'http://auth', 'state')
        mock_post.return_value = Mock(status_code=401, headers={})
        self.assertEqual(
            obtain_token_via_basic_auth_pkce('client', 'user', 'pass'), {})

    @patch('PyViCare.PyViCareOAuthManager.OAuth2Session')
    @patch('PyViCare.PyViCareOAuthManager.requests.post')
    def test_returns_empty_on_token_exchange_failure(self, mock_post, mock_oauth_cls):
        mock_oauth = Mock()
        mock_oauth.create_authorization_url.return_value = ('http://auth', 'state')
        mock_oauth.fetch_token.side_effect = requests.RequestException("fail")
        mock_oauth_cls.return_value = mock_oauth

        mock_post.return_value = Mock(
            status_code=302,
            headers={'Location': 'vicare://oauth-callback/everest?code=xyz'},
        )
        self.assertEqual(
            obtain_token_via_basic_auth_pkce('client', 'user', 'pass'), {})

    @patch('PyViCare.PyViCareOAuthManager.OAuth2Session')
    @patch('PyViCare.PyViCareOAuthManager.requests.post')
    def test_returns_empty_on_authlib_oauth_error(self, mock_post, mock_oauth_cls):
        mock_oauth = Mock()
        mock_oauth.create_authorization_url.return_value = ('http://auth', 'state')
        mock_oauth.fetch_token.side_effect = OAuthError("invalid_grant")
        mock_oauth_cls.return_value = mock_oauth

        mock_post.return_value = Mock(
            status_code=302,
            headers={'Location': 'vicare://oauth-callback/everest?code=xyz'},
        )
        self.assertEqual(
            obtain_token_via_basic_auth_pkce('client', 'user', 'pass'), {})
