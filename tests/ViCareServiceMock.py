from PyViCare.PyViCareService import (ViCareDeviceAccessor,
                                      buildSetPropertyUrl, readFeature)
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


class ViCareServiceMock:

    def __init__(self, filename, rawInput=None):
        if rawInput is None:
            testData = readJson(filename)
            self.testData = testData
        else:
            self.testData = rawInput

        self.setPropertyData = []

    def getProperty(self, accessor: ViCareDeviceAccessor, property_name):
        entities = self.testData["data"]
        return readFeature(entities, property_name)

    def setProperty(self, accessor: ViCareDeviceAccessor, property_name, action, data):
        self.setPropertyData.append({
            "url": buildSetPropertyUrl(accessor, property_name, action),
            "property_name": property_name,
            "action": action,
            "data": data
        })
