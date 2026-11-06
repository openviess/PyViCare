import json
import os
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests
from authlib.integrations.requests_client import OAuth2Session

from PyViCare.PyViCareAbstractOAuthManager import TOKEN_URL
from PyViCare.PyViCareBrowserOAuthManager import ViCareBrowserOAuthManager


class ViCareBrowserOAuthManagerTest(unittest.TestCase):

    def setUp(self):
        self.stored_token = {
            'access_token': 'expired-access-token',
            'token_type': 'Bearer',
            'expires_in': 0,
            'refresh_token': 'stored-refresh-token',
        }

    def _create_manager_with_stored_token(self):
        oauth_session = OAuth2Session('client_id', token=self.stored_token)
        with tempfile.TemporaryDirectory() as temp_dir:
            token_file = os.path.join(temp_dir, 'token.json')
            with open(token_file, mode='w') as json_file:
                json.dump(self.stored_token, json_file)

            with patch('PyViCare.PyViCareBrowserOAuthManager.OAuth2Session', return_value=oauth_session):
                return ViCareBrowserOAuthManager('client_id', token_file)

    def _renew_token_and_capture_request(self):
        manager = self._create_manager_with_stored_token()

        captured_requests = []

        def fake_request(method, url, **kwargs):
            captured_requests.append({'method': method, 'url': url, **kwargs})

            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                'access_token': 'new-access-token',
                'token_type': 'Bearer',
                'refresh_token': 'new-refresh-token',
            }
            return response

        with patch.object(requests.Session, 'request', side_effect=fake_request):
            manager.renewToken()

        return manager, captured_requests

    def test_renew_token_sends_stored_refresh_token_to_token_endpoint(self):
        _, captured_requests = self._renew_token_and_capture_request()

        self.assertEqual(1, len(captured_requests))
        request = captured_requests[0]
        self.assertEqual('POST', request['method'])
        self.assertEqual(TOKEN_URL, request['url'])
        self.assertEqual(
            {'grant_type': 'refresh_token', 'refresh_token': 'stored-refresh-token'},
            request['data'])

    def test_renew_token_updates_session_token(self):
        manager, _ = self._renew_token_and_capture_request()
        self.assertEqual('new-access-token', manager.oauth_session.token['access_token'])
