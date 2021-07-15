from PyViCare.PyViCareService import ViCareService, readFeature, buildSetPropertyUrl
from tests.helper import readJson

class ViCareServiceMock(ViCareService):
    
    def __init__(self, filename, circuit, rawInput = None):
        if rawInput is None:
            testData = readJson(filename)
            self.testData = testData
        else:
            self.testData = rawInput

        self.circuit = circuit
        self.setPropertyData = []

    def getProperty(self, property_name):
        entities = self.testData["data"]
        return readFeature(entities, property_name)

    def setProperty(self, property_name, action, data):
        self.setPropertyData.append({
            "url" : buildSetPropertyUrl('[id]', '[serial]', 0, property_name, action),
            "property_name": property_name,
            "action" : action,
            "data" : data
        })
        