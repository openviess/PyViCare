from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError
import requests
import re
import json
import pickle
import os

client_id = '79742319e39245de5f91d15ff4cac2a8';
client_secret = '8ad97aceb92c5892e102b093c7c083fa';
authorizeURL = 'https://iam.viessmann.com/idp/v1/authorize';
token_url = 'https://iam.viessmann.com/idp/v1/token';
apiURLBase = 'https://api.viessmann-platform.io';
redirect_uri = "vicare://oauth-callback/everest";
viessmann_scope=["openid"]

# TODO Holiday program can still be used (parameters are there) heating.circuits.0.operating.programs.holiday
# TODO set eco program (does not appear to work on my install)
# TODO heating.dhw.schedule/setSchedule slope&shift numbers
# TODO heating.circuits.0.heating.curve/setCurve
# TODO error handling
# TODO documentation
# TODO Detect expired token (coming soon)
#{
#    "error": "EXPIRED TOKEN"
#}

""""Viessmann ViCare API Python tools"""

class PyViCare:
    """This class connects to the Viesmann ViCare API.
    The authentication is done through OAuth2. 
    Note that currently, a new token is generate for each run.
    """

    def __init__(self, username, password,token_file=None):
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
        self.username=username
        self.password=password
        self.token_file=token_file
        self.oauth=self.__restoreToken(username, password,token_file)
        self.getInstallations()
        
    def __restoreToken(self, username, password,token_file=None):
        """Create the necessary oAuth2 sessions
        Viessmann tokens expire after 3600s (60min)
        Parameters
        ----------
        username : str
            e-mail address
        password : str
            password

        Returns
        -------
        oauth: 
            oauth sessions object
        """
        if os.path.isfile(token_file):
            print("reuse token")
            oauth = OAuth2Session(client_id,token=self.deserializeToken(token_file))   
        else:
            oauth = self.getNewToken(username, password,token_file)
        return oauth
        
    def getNewToken(self, username, password,token_file=None):
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,scope=viessmann_scope)
        authorization_url, state = oauth.authorization_url(authorizeURL)
        codestring=""
        try:
            header = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.post(authorization_url, headers=header,auth=(username, password))
        except requests.exceptions.InvalidSchema as e:
            #capture the error, which contains the code the authorization code and put this in to codestring
            codestring = "{0}".format(str(e.args[0])).encode("utf-8");
            codestring = str(codestring)
            match = re.search("code\=(.*)\&",codestring)
            codestring=match.group(1)
            oauth.fetch_token(token_url, client_secret=client_secret,authorization_response=authorization_url,code=codestring)
        if token_file != None:
            print()
            self.serializeToken(oauth.token,token_file)
        return oauth
        
    def __get(self,url):
        try:
            r=self.oauth.get(url).json()
            return r
        except TokenExpiredError as e:
            self.oauth=self.getNewToken(self.username,self.password,self.token_file)
            print("token renewed")
            return self.__get(url)
        
        
    def __post(self,url,data):
        h = {"Content-Type":"application/json","Accept":"application/vnd.siren+json"}
        try:
            j=self.oauth.post(url,data,headers=h)
            try:
                r=j.json()
                return r
            except json.decoder.JSONDecodeError:
                if j.status_code == 204:
                    return json.loads("{\"statusCode\": 204, \"error\": \"None\", \"message\": \"SUCCESS\"}")
                else:
                    return json.loads("{\"statusCode\":"+j.status_code+", \"error\": \"Unknown\", \"message\": \"UNKNOWN\"}")
        except TokenExpiredError as e:
            self.oauth=self.getNewToken(self.username,self.password,self.token_file)
            print("token renewed")
            return self._post(url,data)    
    
    def serializeToken(self,oauth,token_file):
        binary_file = open(token_file,mode='wb')
        s_token = pickle.dump(oauth,binary_file)
        binary_file.close()
        print(s_token)
        
    def deserializeToken(self,token_file):
        binary_file = open(token_file,mode='rb')
        s_token = pickle.load(binary_file)
        return s_token
    
    def getInstallations(self):
        self.installations = self.__get(apiURLBase+"/general-management/installations?expanded=true&")
        self.href=self.installations["entities"][0]["links"][0]["href"]
        self.id=self.installations["entities"][0]["properties"]["id"]
        self.serial=self.installations["entities"][0]["entities"][0]["properties"]["serial"]
        return self.installations
    
    def getProperty(self,property_name):
        url = apiURLBase + '/operational-data/installations/' + str(self.id) + '/gateways/' + str(self.serial) + '/devices/0/features/' + property_name
        j=self.__get(url)
        return j
    
    def setProperty(self,property_name,action,data):
        url = apiURLBase + '/operational-data/v1/installations/' + str(self.id) + '/gateways/' + str(self.serial) + '/devices/0/features/' + property_name +"/"+action
        return self.__post(url,data)
        
    def setMode(self,mode):
        r=self.setProperty("heating.circuits.0.operating.modes.active","setMode","{\"mode\":\""+mode+"\"}")
        return r
    
    # Works for normal, reduced, comfort
    # active has no action
    # exetenral , standby no action
    # holiday, sheculde and unscheduled 
    # activate, decativate comfort,eco
    
    def setProgramTemperature(self,program: str,temperature :int):
        return self.setProperty("heating.circuits.0.operating.programs."+program,"setTemperature","{\"targetTemperature\":"+str(temperature)+"}")
    
    # comfort, eco
    # optional temperature parameter could be passed (but not done)
    def activateProgram(self,program):
        return self.setProperty("heating.circuits.0.operating.programs."+program,"activate","{}")
        
    def deactivateProgram(self,program):
        return self.setProperty("heating.circuits.0.operating.programs."+program,"deactivate","{}")
    
    def setDomesticHotWaterTemperature(self,temperature):
        return self.setProperty("heating.dhw.temperature","setTargetTemperature","{\"temperature\":"+str(temperature)+"}")
    
    def getMonthSinceLastService(self):
        return self.getProperty("heating.service.timeBased")["properties"]["activeMonthSinceLastService"]["value"]
    
    def getLastServiceDate(self):
        return self.getProperty("heating.service.timeBased")["properties"]["lastService"]["value"]
        
    def getOutsideTemperature(self):
        r=self.getProperty("heating.sensors.temperature.outside")
        return r["properties"]["value"]["value"]
        
    def getSupplyTemperature(self):
        return self.getProperty("heating.circuits.0.sensors.temperature.supply")["properties"]["value"]["value"]
    
    def getRoomTemperature(self):
        return self.getProperty("heating.circuits.0.sensors.temperature.room")["properties"]["value"]["value"]
        
    def getModes(self):
        return self.getProperty("heating.circuits.0.operating.modes.active")["actions"][0]["fields"][0]["enum"]
        
    def getActiveMode(self):
        return self.getProperty("heating.circuits.0.operating.modes.active")["properties"]["value"]["value"]
        
    def getHeatingCurveShift(self):
        return self.getProperty("heating.circuits.0.heating.curve")["properties"]["shift"]["value"]
    
    def getHeatingCurveSlope(self):
        return self.getProperty("heating.circuits.0.heating.curve")["properties"]["slope"]["value"]
        
    def getBoilerTemperature(self):
        r=self.getProperty("heating.boiler.sensors.temperature.main")
        return r["properties"]["value"]["value"]
    
    def getActiveProgram(self):
        r=self.getProperty("heating.circuits.0.operating.programs.active")
        return r["properties"]["value"]["value"]
    
    def getPrograms(self):
        r=self.getProperty("heating.circuits.0.operating.programs")
        return r["entities"][9]["properties"]["components"]
        
    def getDesiredTemperatureForProgram(self , program):
        r=self.getProperty("heating.circuits.0.operating.programs."+program)
        return r["properties"]["temperature"]["value"]
        
    def setDesiredTemperatureForProgram(self,program,temperature):
        print("o")
        
    def getCurrentDesiredTemperature(self):
        r=self.getProperty("heating.circuits.0.operating.programs."+self.getActiveProgram())
        return r["properties"]["temperature"]["value"]
        
    def getDomesticHotWaterConfiguredTemperature(self):
        r=self.getProperty("heating.dhw.temperature")
        return r["properties"]["value"]["value"]
        
    def getDomesticHotWaterStorageTemperature(self):
        return self.getProperty("heating.dhw.sensors.temperature.hotWaterStorage")["properties"]["value"]["value"]  
        
    def getDomesticHotWaterMaxTemperature(self):
        return self.getProperty("heating.dhw.temperature")["actions"][0]["fields"][0]["max"]
    
    def getDomesticHotWaterMinTemperature(self):
        return self.getProperty("heating.dhw.temperature")["actions"][0]["fields"][0]["min"]