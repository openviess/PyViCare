from PyViCare.PyViCareService import ViCareDeviceAccessor, readFeature, buildSetPropertyUrl
from tests.helper import readJson

class ViCareServiceMock:
    
    def __init__(self, filename, circuit, rawInput = None):
        if rawInput is None:
            testData = readJson(filename)
            self.testData = testData
        else:
            self.testData = rawInput

        self.accessor = ViCareDeviceAccessor(
                        '[id]', '[serial]', circuit)
        self.setPropertyData = []

    def getProperty(self, property_name):
        entities = self.testData["data"]
        return readFeature(entities, property_name)

    def setProperty(self, property_name, action, data):
        self.setPropertyData.append({
            "url" : buildSetPropertyUrl(self.accessor.id, self.accessor.serial, self.accessor.circuit, property_name, action),
            "property_name": property_name,
            "action" : action,
            "data" : data
        })
        