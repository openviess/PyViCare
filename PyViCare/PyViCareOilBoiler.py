from PyViCare.PyViCareDevice import Device

class OilBoiler(Device):

    def getBurnerActive(self):
        try:
            return self.service.getProperty("heating.burner")["properties"]["active"]["value"]
        except KeyError:
            return "error"
            
    def getBurnerModulation(self):
        try:
            return self.service.getProperty('heating.burner.modulation')["properties"]["value"]["value"]
        except KeyError:
            return "error"   
            
    def getBoilerTemperature(self):
        try:
            return self.service.getProperty("heating.boiler.sensors.temperature.main")["properties"]["value"]["value"]
        except KeyError:
            return "error"
    
    def getBurnerHours(self):
        try:
            return self.service.getProperty('heating.burner.statistics')['properties']['hours']['value']
        except KeyError:
            return "error"

    def getBurnerStarts(self):
        try:
            return self.service.getProperty('heating.burner.statistics')['properties']['starts']['value']
        except KeyError:
            return "error"
