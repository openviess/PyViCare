from PyViCare.PyViCareService import (ViCareDeviceAccessor, readFeature)
from tests.helper import readJson


def MockCircuitsData(circuits):
    return {
        "properties": {
            "enabled": {
                "value": circuits
            }
        },
        "feature": "heating.circuits",
    }


class ViCareGatewayServiceMock:

    def __init__(self, filename, rawInput=None):
        if rawInput is None:
            testData = readJson(filename)
            self.testData = testData
        else:
            self.testData = rawInput

        self.accessor = ViCareDeviceAccessor('[id]', '[serial]', '[deviceid]')
        self.setPropertyData = []

    def getProperty(self, property_name):
        entities = self.testData["data"]
        return readFeature(entities, property_name)

    # def setProperty(self, property_name, action, data):
    #     self.setPropertyData.append({
    #         "url": buildSetPropertyUrl(self.accessor, property_name, action),
    #         "property_name": property_name,
    #         "action": action,
    #         "data": data
    #     })
