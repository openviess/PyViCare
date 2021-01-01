import simplejson as json
import os
from PyViCare.PyViCareService import ViCareService

class ViCareServiceForTesting(ViCareService):
    
    def __init__(self, filename, circuit):
        test_filename = os.path.join(os.path.dirname(__file__), filename)
        try:
            json_file = open(test_filename, mode='rb')
            testData = json.load(json_file)
        finally:
            json_file.close()
        self.testData = testData
        self.circuit = circuit
        self.setPropertyData = []

    def getProperty(self, property_name):
        entities = self.testData["entities"]
        feature = next((f for f in entities if f["class"][0] == property_name and f["class"][1] == "feature"), {})
        return feature

    def setProperty(self, property_name, action, data):
        self.setPropertyData.append({
            "property_name": property_name,
            "action" : action,
            "data" : data
        })
        