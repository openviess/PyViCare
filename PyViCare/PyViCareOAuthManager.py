from PyViCare import Feature
from PyViCare.PyViCareUtils import PyViCareRateLimitError
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

authorizeURL = 'https://iam.viessmann.com/idp/v2/authorize'
token_url = 'https://iam.viessmann.com/idp/v2/token'
redirect_uri = "vicare://oauth-callback/everest"
viessmann_scope = ["IoT User"]
apiURLBase = 'https://api.viessmann.com/iot/v1'



class AbstractViCareOAuthManager:
    def __init__(self):
        self.oauth = None

    @abstractclassmethod
    def renewToken(self):
        return

    def get(self, url):
        try:
            logger.debug(self.oauth)
            response = self.oauth.get(apiURLBase + url).json()
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
                apiURLBase + url, data, headers=headers).json()
            self.handleExpiredToken(response)
            self.handleRateLimit(response)
            return response
        except TokenExpiredError:
            self.oauth_manager.renewToken()
            return self.post(url, data)


class ViCareHomeAssistantOAuthManager(AbstractViCareOAuthManager):
    def __init__(self, oauth):
        self.oauth = oauth

    def renewToken(self):
        # todo
        return super().renewToken()


class ViCareOAuthManager(AbstractViCareOAuthManager):
    def __init__(self, username, password, client_id, token_file):
        self.username = username
        self.password = password
        self.token_file = token_file
        self.client_id = client_id
        self.oauth = self.__restore_oauth_session_from_token(token_file)

    def __restore_oauth_session_from_token(self, token_file):
        """Create the necessary oAuth2 sessions
        Restore it from token_file if existing (token dict)
        Viessmann tokens expire after 3600s (60min)
        Parameters
        ----------
        username : str
            e-mail address
        password : str
            password
        token_file: str
            path to serialize the token (will restore if already existing)

        Returns
        -------
        oauth:
            oauth sessions object
        """
        if (token_file != None) and os.path.isfile(token_file):
            try:
                logger.info("Token file exists")
                oauth = OAuth2Session(
                    self.client_id, token=self._deserializeToken(token_file))
                logger.info("Token restored from file")
                return oauth
            except UnpicklingError:
                logger.warning("Could not restore token")

        logger.debug("Token file argument not provided or file does not exist")
        oauth = self.__getNewToken(self.username, self.password, token_file)
        return oauth

    def __getNewToken(self, username, password, token_file=None):
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
            self.client_id, redirect_uri=redirect_uri, scope=viessmann_scope)
        authorization_url, _ = oauth.authorization_url(authorizeURL)

        # workaround until requests-oauthlib supports PKCE flow
        code_verifier, code_challenge = pkce.generate_pkce_pair()
        authorization_url += '&code_challenge=' + \
            code_challenge + '&code_challenge_method=S256'
        logger.debug("Auth URL is: "+authorization_url)

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
            logger.debug("Codestring : "+codestring)

            # workaround until requests-oauthlib supports PKCE flow
            resp = requests.post(url=token_url,
                                 data={
                                     'grant_type': 'authorization_code',
                                     'client_id': self.client_id,
                                     'redirect_uri': redirect_uri,
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
            logger.debug("Token received: ")
            logger.debug(oauth)
            logger.debug("Start serial")
            if token_file != None:
                self._serializeToken(oauth.token, token_file)
                logger.info("Token serialized to "+token_file)
            logger.info("New token created")
            return oauth

    def renewToken(self):
        logger.info("Token expired, renewing")
        self.oauth = self.__getNewToken(
            self.username, self.password, self.token_file)
        logger.info("Token renewed successfully")

    def _serializeToken(self, oauth, token_file):
        binary_file = open(token_file, mode='wb')
        try:
            pickle.dump(oauth, binary_file)
        finally:
            binary_file.close()

    def _deserializeToken(self, token_file):
        binary_file = open(token_file, mode='rb')
        try:
            s_token = pickle.load(binary_file)
            return s_token
        finally:
            binary_file.close()
