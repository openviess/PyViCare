from PyViCare import Feature
from PyViCare.PyViCareUtils import PyViCareInvalidCredentialsError, PyViCareRateLimitError
from abc import abstractclassmethod
from oauthlib.oauth2 import TokenExpiredError
import requests
import re
import pickle
import os
import pkce
from pickle import UnpicklingError
from requests_oauthlib import OAuth2Session
import logging

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

AUTHORIZE_URL = 'https://iam.viessmann.com/idp/v2/authorize'
TOKEN_URL = 'https://iam.viessmann.com/idp/v2/token'
REDIRECT_URI = "vicare://oauth-callback/everest"
VIESSMANN_SCOPE = ["IoT User"]
API_BASE_URL = 'https://api.viessmann.com/iot/v1'


class AbstractViCareOAuthManager:
    def __init__(self):
        self.oauth = None

    @abstractclassmethod
    def renewToken(self):
        return

    def get(self, url):
        try:
            logger.debug(self.oauth)
            response = self.oauth.get(f"{API_BASE_URL}{url}").json()
            logger.debug("Response to get request: "+str(response))
            self.handleExpiredToken(response)
            self.handleRateLimit(response)
            return response
        except TokenExpiredError:
            self.renewToken()
            return self.get(url)

    def handleExpiredToken(self, response):
        if("error" in response and response["error"] == "EXPIRED TOKEN"):
            raise TokenExpiredError(response)

    def handleRateLimit(self, response):
        if not Feature.raise_exception_on_rate_limit:
            return

        if("statusCode" in response and response["statusCode"] == 429):
            raise PyViCareRateLimitError(response)

    """POST URL using OAuth session. Automatically renew the token if needed
    Parameters
    ----------
    url : str
        URL to get
    data : str
        Data to post

    Returns
    -------
    result: json
        json representation of the answer
    """

    def post(self, url, data):
        headers = {"Content-Type": "application/json",
                   "Accept": "application/vnd.siren+json"}
        try:
            response = self.oauth.post(
                f"{API_BASE_URL}{url}", data, headers=headers).json()
            self.handleExpiredToken(response)
            self.handleRateLimit(response)
            return response
        except TokenExpiredError:
            self.renewToken()
            return self.post(url, data)


class ViCareHomeAssistantOAuthManager(AbstractViCareOAuthManager):
    def __init__(self, oauth):
        self.oauth = oauth

    def renewToken(self):
        # todo: move this class to Home Assistant and implement the oauth flow
        return super().renewToken()


class ViCareOAuthManager(AbstractViCareOAuthManager):
    def __init__(self, username, password, client_id, token_file):
        self.username = username
        self.password = password
        self.token_file = token_file
        self.client_id = client_id
        self.oauth = self.__restore_oauth_session_from_token(token_file)

    def __restore_oauth_session_from_token(self, token_file):
        existing_token = self._deserializeToken(token_file)
        if existing_token is not None:
            return OAuth2Session(self.client_id, token=existing_token)

        return self.__createNewSession(self.username, self.password, token_file)

    def __createNewSession(self, username, password, token_file=None):
        """Create a new oAuth2 sessions
        Viessmann tokens expire after 3600s (60min)
        Parameters
        ----------
        username : str
            e-mail address
        password : str
            password
        token_file: str
            path to serialize the token (will restore if already existing). No serialisation if not present

        Returns
        -------
        oauth:
            oauth sessions object
        """
        oauth = OAuth2Session(
            self.client_id, redirect_uri=REDIRECT_URI, scope=VIESSMANN_SCOPE)
        base_authorization_url, _ = oauth.authorization_url(AUTHORIZE_URL)

        # workaround until requests-oauthlib supports PKCE flow
        code_verifier, code_challenge = pkce.generate_pkce_pair()
        authorization_url = f'{base_authorization_url}&code_challenge={code_challenge}&code_challenge_method=S256'
        logger.debug(f"Auth URL is: {authorization_url}")

        try:
            header = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.post(
                authorization_url, headers=header, auth=(username, password))
            logger.warning(
                "Received an HTML answer from the server during auth, this is not normal:")
            logger.debug(response.content)
        except requests.exceptions.InvalidSchema as e:
            # capture the error, which contains the code the authorization code and put this in to codestring
            codestring = "{0}".format(str(e.args[0])).encode("utf-8")
            codestring = str(codestring)
            match = re.search("code=(.*)&", codestring)
            codestring = match.group(1)
            logger.debug(f"Codestring : {codestring}")

            # workaround until requests-oauthlib supports PKCE flow
            resp = requests.post(url=TOKEN_URL, data={
                'grant_type': 'authorization_code',
                'client_id': self.client_id,
                'redirect_uri': REDIRECT_URI,
                'code': codestring,
                'code_verifier': code_verifier
            }
            )
            result = resp.json()
            token_dict = {
                'access_token': result['access_token'],
                'token_type': 'bearer'
            }
            oauth = OAuth2Session(client_id=self.client_id, token=token_dict)
            logger.debug(f"Token received: {oauth.token}")
            self._serializeToken(oauth.token, token_file)
            logger.info("New token created")
            return oauth
        raise PyViCareInvalidCredentialsError()

    def renewToken(self):
        logger.info("Token expired, renewing")
        self.oauth = self.__createNewSession(
            self.username, self.password, self.token_file)
        logger.info("Token renewed successfully")

    def _serializeToken(self, oauth, token_file):
        logger.debug("Start serial")
        if token_file is None:
            logger.debug("Skip serial, no file provided.")
            return

        with open(token_file, mode='wb') as binary_file:
            pickle.dump(oauth, binary_file)

        logger.info("Token serialized to %s" % token_file)

    def _deserializeToken(self, token_file):
        if (token_file == None) or not os.path.isfile(token_file):
            logger.debug(
                "Token file argument not provided or file does not exist")
            return None

        logger.info("Token file exists")
        try:
            with open(token_file, mode='rb') as binary_file:
                s_token = pickle.load(binary_file)
                logger.info("Token restored from file")
                return s_token
        except UnpicklingError:
            pass
        logger.warning("Could not restore token")
        return None
