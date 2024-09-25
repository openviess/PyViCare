import logging
import os
import pickle
from contextlib import suppress
from pickle import UnpicklingError

import requests
from authlib.common.security import generate_token
from authlib.integrations.requests_client import OAuth2Session

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareUtils import (PyViCareInvalidConfigurationError,
                                    PyViCareInvalidCredentialsError)

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())

AUTHORIZE_URL = 'https://iam.viessmann.com/idp/v3/authorize'
TOKEN_URL = 'https://iam.viessmann.com/idp/v3/token'
REDIRECT_URI = "vicare://oauth-callback/everest"
VIESSMANN_SCOPE = ["IoT User"]


class ViCareOAuthManager(AbstractViCareOAuthManager):
    def __init__(self, username, password, client_id, token_file):
        self.username = username
        self.password = password
        self.token_file = token_file
        self.client_id = client_id
        oauth_session = self.__restore_oauth_session_from_token(token_file)
        super().__init__(oauth_session)

    def __restore_oauth_session_from_token(self, token_file):
        existing_token = self.__deserialize_token(token_file)
        if existing_token is not None:
            return OAuth2Session(self.client_id, token=existing_token)

        return self.__create_new_session(self.username, self.password, token_file)

    def __create_new_session(self, username, password, token_file=None):
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
        oauth_session = OAuth2Session(
            self.client_id, redirect_uri=REDIRECT_URI, scope=VIESSMANN_SCOPE, code_challenge_method='S256')
        code_verifier = generate_token(48)
        authorization_url, _ = oauth_session.create_authorization_url(AUTHORIZE_URL, code_verifier=code_verifier)
        logger.debug("Auth URL is: %s", authorization_url)

        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(
            authorization_url, headers=header, auth=(username, password), allow_redirects=False)

        if response.status_code == 401:
            raise PyViCareInvalidConfigurationError(response.json())

        if 'Location' not in response.headers:
            logger.debug('Response: %s', response)
            raise PyViCareInvalidCredentialsError()

        oauth_session.fetch_token(TOKEN_URL, authorization_response=response.headers['Location'], code_verifier=code_verifier)

        if oauth_session.token is None:
            raise PyViCareInvalidCredentialsError()

        logger.debug("Token received: %s",oauth_session.token)
        self.__serialize_token(oauth_session.token, token_file)
        logger.info("New token created")
        return oauth_session

    def renewToken(self):
        logger.info("Token expired, renewing")
        self.replace_session(self.__create_new_session(
            self.username, self.password, self.token_file))
        logger.info("Token renewed successfully")

    def __serialize_token(self, oauth, token_file):
        logger.debug("Start serial")
        if token_file is None:
            logger.debug("Skip serial, no file provided.")
            return

        with open(token_file, mode='wb') as binary_file:
            pickle.dump(oauth, binary_file)

        logger.info("Token serialized to %s", token_file)

    def __deserialize_token(self, token_file):
        if token_file is None or not os.path.isfile(token_file):
            logger.debug(
                "Token file argument not provided or file does not exist")
            return None

        logger.info("Token file exists")
        with suppress(UnpicklingError):
            with open(token_file, mode='rb') as binary_file:
                s_token = pickle.load(binary_file)
                logger.info("Token restored from file")
                return s_token
        logger.warning("Could not restore token")
        return None
