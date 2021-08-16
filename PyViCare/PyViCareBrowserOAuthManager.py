import json
import logging
import os
import re
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import pkce
import requests
from requests_oauthlib import OAuth2Session

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareUtils import (PyViCareBrowserOAuthTimeoutReachedError,
                                    PyViCareInvalidCredentialsError)

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

AUTHORIZE_URL = 'https://iam.viessmann.com/idp/v2/authorize'
TOKEN_URL = 'https://iam.viessmann.com/idp/v2/token'
REDIRECT_PORT = 51125
VIESSMANN_SCOPE = ["IoT User", "offline_access"]
API_BASE_URL = 'https://api.viessmann.com/iot/v1'
AUTH_TIMEOUT = 60 * 3


class ViCareBrowserOAuthManager(AbstractViCareOAuthManager):
    class Serv(BaseHTTPRequestHandler):
        def __init__(self, callback, *args):
            self.callback = callback
            BaseHTTPRequestHandler.__init__(self, *args)

        def do_GET(self):
            (status_code, text) = self.callback(self.path)
            self.send_response(status_code)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(text.encode("utf-8"))

    def __init__(self, client_id: str, token_file: str) -> None:

        self.token_file = token_file
        self.client_id = client_id
        oauth_session = self.__load_or_create_new_session()
        super().__init__(oauth_session)

    def __load_or_create_new_session(self):
        restore_oauth = self.__restoreToken()
        if restore_oauth is not None:
            return restore_oauth
        return self.__execute_browser_authentication()

    def __execute_browser_authentication(self):
        redirect_uri = f"http://localhost:{REDIRECT_PORT}"
        oauth = OAuth2Session(
            self.client_id, redirect_uri=redirect_uri, scope=VIESSMANN_SCOPE)
        base_authorization_url, state = oauth.authorization_url(AUTHORIZE_URL)
        code_verifier, code_challenge = pkce.generate_pkce_pair()
        authorization_url = f'{base_authorization_url}&code_challenge={code_challenge}&code_challenge_method=S256'

        webbrowser.open(authorization_url)

        code = None

        def callback(path):
            nonlocal code
            nonlocal state
            match = re.match(r"(?P<uri>.+?)\?code=(?P<code>.+)&state=(?P<state>.+)", path)
            if match.group('state') != state:
                logger.warn("Invalid OAuth state")
                return (401, "Invalid Oauth state.")
            code = match.group('code')
            return (200, "Success. You can close this browser window now.")

        def handlerWithCallbackWrapper(*args):
            ViCareBrowserOAuthManager.Serv(callback, *args)

        server = HTTPServer(('localhost', REDIRECT_PORT),
                            handlerWithCallbackWrapper)
        server.timeout = AUTH_TIMEOUT
        server.handle_request()

        if code is None:
            logger.debug("Timeout reached")
            raise PyViCareBrowserOAuthTimeoutReachedError()

        logger.debug(f"Code: {code}")

        result = requests.post(url=TOKEN_URL, data={
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'code': code,
            'code_verifier': code_verifier
        }
        ).json()

        return self.__build_oauth_session(result, after_redirect=True)

    def __storeToken(self, token):
        if self.token_file is None:
            return

        with open(self.token_file, mode='w') as json_file:
            json.dump(token, json_file)
            logger.info("Token stored to file")

    def __restoreToken(self):
        if self.token_file is None or not os.path.isfile(self.token_file):
            return None

        with open(self.token_file, mode='r') as json_file:
            token = json.load(json_file)
            logger.info("Token restored from file")
            return self.__build_oauth_session(token, after_redirect=False)

    def __build_oauth_session(self, result, after_redirect):
        if 'access_token' not in result and 'refresh_token' not in result:
            logger.debug(f"Invalid result after redirect {result}")
            if after_redirect:
                raise PyViCareInvalidCredentialsError()
            else:
                logger.info("Invalid credentials, create new session")
                return self.__execute_browser_authentication()

        logger.debug(f"configure oauth: {result}")
        self.__storeToken(result)
        return OAuth2Session(client_id=self.client_id, token=result)

    def renewToken(self) -> None:
        token = self.oauth_session.token
        result = requests.post(url=TOKEN_URL, data={
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'refresh_token': token['refresh_token'],
        }
        ).json()

        self.replace_session(self.__build_oauth_session(result, after_redirect=False))
