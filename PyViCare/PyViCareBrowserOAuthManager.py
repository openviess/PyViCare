from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare import Feature
from PyViCare.PyViCareUtils import PyViCareInvalidCredentialsError, PyViCareRateLimitError
from abc import abstractclassmethod
from oauthlib.oauth2 import TokenExpiredError
import requests
import re
import pickle
import threading
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
REDIRECT_URI = "http://localhost:5125"
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
            self.wfile.write("Success. You can close this browser window now.".encode("utf-8"))
            
    def __init__(self, client_id, token_file):
        self.token_file = token_file
        self.client_id = client_id
        self.abc = self.__createNewSession()

    def __createNewSession(self):

        oauth = OAuth2Session(
            self.client_id, redirect_uri=REDIRECT_URI, scope=VIESSMANN_SCOPE)
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

        server = HTTPServer(('localhost',5125), handlerWithCallbackWrapper)
        server.serve_forever()
        print(f"Code: {code}")

    def renewToken(self):

        offline_access

        # todo: move this class to Home Assistant and implement the oauth flow
        return super().renewToken()
