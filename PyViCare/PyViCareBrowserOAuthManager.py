import json
import logging
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

from authlib.common.security import generate_token
from authlib.integrations.requests_client import OAuth2Session

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareUtils import (PyViCareBrowserOAuthTimeoutReachedError,
                                    PyViCareInvalidCredentialsError)

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

AUTHORIZE_URL = 'https://iam.viessmann.com/idp/v3/authorize'
TOKEN_URL = 'https://iam.viessmann.com/idp/v3/token'
REDIRECT_PORT = 51125
VIESSMANN_SCOPE = ["IoT User", "offline_access"]
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
        oauth_session = OAuth2Session(
            self.client_id, redirect_uri=redirect_uri, scope=VIESSMANN_SCOPE, code_challenge_method='S256')
        code_verifier = generate_token(48)
        authorization_url, _ = oauth_session.create_authorization_url(AUTHORIZE_URL, code_verifier=code_verifier)

        webbrowser.open(authorization_url)

        location = None

        def callback(path):
            nonlocal location
            location = path
            return (200, "Success. You can close this browser window now.")

        def handlerWithCallbackWrapper(*args):
            ViCareBrowserOAuthManager.Serv(callback, *args)

        server = HTTPServer(('localhost', REDIRECT_PORT),
                            handlerWithCallbackWrapper)
        server.timeout = AUTH_TIMEOUT
        server.handle_request()

        if location is None:
            logger.debug("Timeout reached")
            raise PyViCareBrowserOAuthTimeoutReachedError()

        logger.debug("Location: %s", location)

        oauth_session.fetch_token(TOKEN_URL, authorization_response=location, code_verifier=code_verifier)

        if oauth_session.token is None:
            raise PyViCareInvalidCredentialsError()

        logger.debug("Token received: %s", oauth_session.token)
        self.__storeToken(oauth_session.token)
        logger.info("New token created")
        return oauth_session

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
            return OAuth2Session(self.client_id, token=token)

    def renewToken(self) -> None:  # type: ignore
        refresh_token = self.oauth_session.refresh_token
        self.oauth_session.refresh_token(TOKEN_URL, refresh_token=refresh_token)
