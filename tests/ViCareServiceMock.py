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

    def __init__(self, roles, filename, rawInput=None):
        if rawInput is None:
            testData = readJson(filename)
            self.testData = testData
        else:
            self.testData = rawInput

        self.roles = roles
        self.accessor = ViCareDeviceAccessor(
            '[id]', '[serial]', '[deviceid]')
        self.setPropertyData = []

    def hasRoles(self, requested_roles) -> bool:
        return len(requested_roles) > 0 and set(requested_roles).issubset(set(self.roles))

    def getProperty(self, property_name):
        entities = self.testData["data"]
        return readFeature(entities, property_name)

    def setProperty(self, property_name, action, data):
        self.setPropertyData.append({
            "url": buildSetPropertyUrl(self.accessor, property_name, action),
            "property_name": property_name,
            "action": action,
            "data": data
        })
