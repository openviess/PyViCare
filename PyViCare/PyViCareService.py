import logging

from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError

logger = logging.getLogger('ViCare')
logger.addHandler(logging.NullHandler())


def readFeature(entities, property_name):
    feature = next(
        (f for f in entities if f["feature"] == property_name), None)

    if(feature is None):
        raise PyViCareNotSupportedFeatureError(property_name)

    return feature


def buildSetPropertyUrl(id, serial, circuit, property_name, action):
    return '/equipment/installations/'+str(id)+'/gateways/'+str(serial)+'/devices/'+str(circuit)+'/features/'+property_name+'/'+action


def buildGetPropertyUrl(id, serial, circuit, property_name):
    return '/equipment/installations/'+str(id)+'/gateways/'+str(serial)+'/devices/'+str(circuit)+'/features/'+property_name

class ViCareDeviceAccessor:
    def __init__(self, id, serial, circuit):
        self.id = id
        self.serial = serial
        self.circuit = circuit


class ViCareService:
    def __init__(self, oauth_manager, accessor):
        self.oauth_manager = oauth_manager
        self.accessor = accessor

    def getProperty(self, property_name):
        url = buildGetPropertyUrl(
            self.accessor.id, self.accessor.serial, self.accessor.circuit, property_name)
        j = self.oauth_manager.get(url)
        return j

    def setProperty(self, property_name, action, data):
        url = buildSetPropertyUrl(
            self.accessor.id, self.accessor.serial, self.accessor.circuit, property_name, action)
        return self.oauth_manager.post(url, data)