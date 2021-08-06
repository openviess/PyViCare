from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare import Feature
from PyViCare.PyViCareUtils import PyViCareInvalidCredentialsError, PyViCareRateLimitError
from abc import abstractclassmethod
from oauthlib.oauth2 import TokenExpiredError
import requests
import re
import pickle
import threading
import json
import os
import pkce
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from requests_oauthlib import OAuth2Session
import webbrowser

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

AUTHORIZE_URL = 'https://iam.viessmann.com/idp/v2/authorize'
TOKEN_URL = 'https://iam.viessmann.com/idp/v2/token'
REDIRECT_PORT = 51125
VIESSMANN_SCOPE = ["IoT User", "offline_access"]
API_BASE_URL = 'https://api.viessmann.com/iot/v1'


class ViCareBrowserOAuthManager(AbstractViCareOAuthManager):
    class Serv(BaseHTTPRequestHandler):
        def __init__(self, callback, *args):
            self.callback = callback
            BaseHTTPRequestHandler.__init__(self, *args)

        def do_GET(self):
            self.callback(self.path)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(
                "Success. You can close this browser window now.".encode("utf-8"))

    def __init__(self, client_id, token_file):
        super().__init__()
        self.token_file = token_file
        self.client_id = client_id
        self.token = None
        self.oauth = None
        self.__loadOrCreateNewSession()

    def __loadOrCreateNewSession(self):
        self.__restoreToken()
        if(self.token is None):
            self.__createNewSession()

    def __createNewSession(self):
        redirect_uri = f"http://localhost:{REDIRECT_PORT}"
        oauth = OAuth2Session(
            self.client_id, redirect_uri=redirect_uri, scope=VIESSMANN_SCOPE)
        base_authorization_url, _ = oauth.authorization_url(AUTHORIZE_URL)
        code_verifier, code_challenge = pkce.generate_pkce_pair()
        authorization_url = f'{base_authorization_url}&code_challenge={code_challenge}&code_challenge_method=S256'

        webbrowser.open(authorization_url)

        server = None
        code = None

        def callback(path):
            nonlocal code
            nonlocal server
            match = re.match(r"(?P<uri>.+?)\?code=(?P<code>[^&]+)", path)
            code = match.group('code')
            threading.Thread(target=server.shutdown, daemon=True).start()

        def handlerWithCallbackWrapper(*args):
            ViCareBrowserOAuthManager.Serv(callback, *args)

        server = HTTPServer(('localhost', REDIRECT_PORT),
                            handlerWithCallbackWrapper)
        server.serve_forever()

        logger.debug(f"Code: {code}")

        result = requests.post(url=TOKEN_URL, data={
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'code': code,
            'code_verifier': code_verifier
        }
        ).json()

        self.__set_oauth(result)

    def __storeToken(self, token):
        with open(self.token_file, mode='w') as json_file:
            token = json.dump(token, json_file)
            logger.info("Token restored from file")
            return token

    def __restoreToken(self):
        if (self.token_file == None) or not os.path.isfile(self.token_file):
            return None

        with open(self.token_file, mode='r') as json_file:
            token = json.load(json_file)
            logger.info("Token restored from file")
            self.__set_oauth(token)
            self.token = token

    def __set_oauth(self, result):
        if 'access_token' not in result and 'refresh_token' not in result:
            logger.debug(f"Invalid result after redirect {result}")
            raise PyViCareInvalidCredentialsError()

        logger.debug(f"configure oauth: {result}")
        self.token = result
        token_dict = {
            'access_token': result['access_token'],
            'token_type': result['token_type']
        }
        self.oauth = OAuth2Session(client_id=self.client_id, token=token_dict)
        self.__storeToken(self.token)

    def renewToken(self):
        result = requests.post(url=TOKEN_URL, data={
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'refresh_token': self.token['refresh_token'],
        }
        ).json()

        self.__set_oauth(result)
