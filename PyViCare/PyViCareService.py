from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError 

import requests
import re
import pickle
import os
import logging
import datetime
import pkce
from pickle import UnpicklingError
# This is required because "requests" uses simplejson if installed on the system 

import simplejson as json
from simplejson import JSONDecodeError
from PyViCare.PyViCare import PyViCareNotSupportedFeatureError, PyViCareRateLimitError
import PyViCare.Feature

authorizeURL = 'https://iam.viessmann.com/idp/v2/authorize'
token_url = 'https://iam.viessmann.com/idp/v2/token'
apiURLBase = 'https://api.viessmann.com/iot/v1'
redirect_uri = "vicare://oauth-callback/everest"
viessmann_scope=["IoT User"]
logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())


def readFeature(entities, property_name):
    feature = next((f for f in entities if f["feature"] == property_name), None)

    if(feature is None):
        raise PyViCareNotSupportedFeatureError(property_name)

    return feature

def buildSetPropertyUrl(id, serial, circuit, property_name, action):
    return apiURLBase +'/equipment/installations/'+str(id)+'/gateways/'+str(serial)+'/devices/'+str(circuit)+'/features/'+property_name+'/'+action

def buildGetPropertyUrl(id, serial, circuit, property_name):
    return apiURLBase + '/equipment/installations/'+str(id)+'/gateways/'+str(serial)+'/devices/'+str(circuit)+'/features/'+property_name   

# https://api.viessmann-platform.io/general-management/v1/installations/DDDDD gives the type like VitoconnectOptolink
# entities / "deviceType": "heating"
# entities are connected devices
# https://api.viessmann-platform.io/general-management/v1/installations/16011/gateways PUT and POST only

# TODO handle multi install / multi devices

""""Viessmann ViCare API Python tools"""

class ViCareService:
    """This class connects to the Viesmann ViCare API.
    The authentication is done through OAuth2.
    Note that currently, a new token is generate for each run.
    """


    def __init__(self, username, password, client_id, token_file=None,circuit=0):
        """Init function. Create the necessary oAuth2 sessions
        Parameters
        ----------
        username : str
            e-mail address
        password : str
            password

        Returns
        -------
        """

        self.username= username
        self.password= password
        self.token_file=token_file
        self.circuit=circuit
        self.client_id = client_id
        self.oauth=self.__restoreToken(token_file)
        self._getInstallations()
        logger.info("Initialisation successful !")

    def __restoreToken(self,token_file=None):
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
        if (token_file!=None) and os.path.isfile(token_file):
            try:
                logger.info("Token file exists")
                oauth = OAuth2Session(self.client_id,token=self._deserializeToken(token_file))
                logger.info("Token restored from file")
            except UnpicklingError:
                logger.warning("Could not restore token")
                oauth = self.__getNewToken(self.username, self.password,token_file)
        else:
            logger.debug("Token file argument not provided or file does not exist")
            oauth = self.__getNewToken(self.username, self.password,token_file)
        return oauth

    def __getNewToken(self, username, password,token_file=None):
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
        oauth = OAuth2Session(self.client_id, redirect_uri=redirect_uri,scope=viessmann_scope)
        authorization_url, _ = oauth.authorization_url(authorizeURL)
           
        # workaround until requests-oauthlib supports PKCE flow
        code_verifier, code_challenge = pkce.generate_pkce_pair()
        authorization_url += '&code_challenge=' + code_challenge + '&code_challenge_method=S256'
        logger.debug("Auth URL is: "+authorization_url)

        try:
            header = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.post(authorization_url, headers=header,auth=(username,password))
            logger.warning("Received an HTML answer from the server during auth, this is not normal:")
            logger.debug(response.content)
        except requests.exceptions.InvalidSchema as e:
            #capture the error, which contains the code the authorization code and put this in to codestring
            codestring = "{0}".format(str(e.args[0])).encode("utf-8")
            codestring = str(codestring)
            match = re.search("code=(.*)&",codestring)
            codestring=match.group(1)
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
            # oauth.fetch_token(token_url, authorization_response=authorization_url,code=codestring)
            logger.debug("Token received: ")
            logger.debug(oauth)
            logger.debug("Start serial")
            if token_file != None:
                self._serializeToken(oauth.token,token_file)
                logger.info("Token serialized to "+token_file)
            logger.info("New token created")
            #TODO throw an exception if oauth is null and implement the auth required method
            # RELLY TODO AttributeError
            return oauth

        # TODO tranform to exception
        
    def renewToken(self):
        logger.info("Token expired, renewing")
        self.oauth=self.__getNewToken(self.username,self.password,self.token_file)
        logger.info("Token renewed successfully")
            
        
    """Get URL using OAuth session. Automatically renew the token if needed
    Parameters
    ----------
    url : str
        URL to get

    Returns
    -------
    result: json
        json representation of the answer
    """
    def __get(self,url):
        try:
            #if(self.oauth==None):
            #    self.renewToken()
            logger.debug(self.oauth)
            r=self.oauth.get(url).json()
            logger.debug("Response to get request: "+str(r))
            self.handleExpiredToken(r)
            self.handleRateLimit(r)
            return r
        except TokenExpiredError:
            self.renewToken()
            return self.__get(url)

    def handleExpiredToken(self, response):
        if("error" in response and response["error"] == "EXPIRED TOKEN"):
            raise TokenExpiredError(response)

    def handleRateLimit(self, response):
        if not PyViCare.Feature.raise_exception_on_rate_limit:
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
    def __post(self,url,data):
        h = {"Content-Type":"application/json","Accept":"application/vnd.siren+json"}
        try:
            #if(self.oauth==None):
            #    self.renewToken()
            j=self.oauth.post(url,data,headers=h)
            try:
                r=j.json()
                self.handleRateLimit(r)
                return r
            except JSONDecodeError:
                if j.status_code == 204:
                    return {"statusCode": 204, "error": "None", "message": "SUCCESS"}
                else:
                    return {"statusCode": j.status_code, "error": "Unknown", "message": "UNKNOWN"}
        except TokenExpiredError:
            self.renewToken()
            return self.__post(url,data)

    def _serializeToken(self,oauth,token_file):
        binary_file = open(token_file,mode='wb')
        try:
            pickle.dump(oauth,binary_file)
        finally:
            binary_file.close()

    def _deserializeToken(self,token_file):
        binary_file = open(token_file,mode='rb')
        try:  
            s_token = pickle.load(binary_file)
            return s_token
        finally:
            binary_file.close()

    def _getInstallations(self):
        self.installations = self.__get(apiURLBase+"/equipment/installations?includeGateways=true")
        installation = self.installations["data"][0]
        self.id = installation["id"]
        self.serial = installation["gateways"][0]["serial"]
        
        return self.installations

    def getInstallations(self):
        return self.installations

    def get(self, url):
        return self.__get(url)

   #TODO should move to device after refactoring 
    def getProperty(self,property_name):
        url = buildGetPropertyUrl(self.id, self.serial, self.circuit, property_name)
        j=self.__get(url)
        return j

    def setProperty(self,property_name,action,data):
        url = buildSetPropertyUrl(self.id, self.serial, self.circuit, property_name, action)
        return self.__post(url,data)

    
