import simplejson as json
import os
from PyViCare.PyViCareService import ViCareService, readFeature, buildSetPropertyUrl

class ViCareServiceForTesting(ViCareService):
    
    def __init__(self, filename, circuit, rawInput = None):
        if rawInput is None:
            test_filename = os.path.join(os.path.dirname(__file__), filename)
            try:
                json_file = open(test_filename, mode='rb')
                testData = json.load(json_file)
            finally:
                json_file.close()
            self.testData = testData
        else:
            self.testData = rawInput

        self.circuit = circuit
        self.setPropertyData = []

    def getProperty(self, property_name):
        entities = self.testData["entities"]
        return readFeature(entities, property_name)

    def setProperty(self, property_name, action, data):
        self.setPropertyData.append({
            "url" : buildSetPropertyUrl('[id]', '[serial]', property_name, action),
            "property_name": property_name,
            "action" : action,
            "data" : data
        })
        