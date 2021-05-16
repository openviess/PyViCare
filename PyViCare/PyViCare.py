import PyViCare.Feature
import datetime
import sys

# This decorator handles access to underlying JSON properties.
# If the property is not found (KeyError) or the index does not 
# exists (IndexError), the requested feature is not supported by 
# the device.
def handleNotSupported(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, IndexError):
            raise PyViCareNotSupportedFeatureError(func.__name__)

    #You can remove that wrapper after the feature flag gets removed entirely.
    def feature_flag_wrapper(*args, **kwargs):
        try:
            return wrapper(*args, **kwargs)
        except PyViCareNotSupportedFeatureError:
            if PyViCare.Feature.raise_exception_on_not_supported_device_feature:
                raise
            else:
                return "error"
    return feature_flag_wrapper

class PyViCareNotSupportedFeatureError(Exception):
    pass

class PyViCareRateLimitError(Exception):

    def __init__(self, response):
        extended_payload = response["extendedPayload"]
        name = extended_payload["name"]
        requestCountLimit = extended_payload["requestCountLimit"]
        limitReset = extended_payload["limitReset"]
        #limitResetDate = datetime.datetime.utcfromtimestamp(limitReset/1000)
        limitResetDate = datetime.datetime.fromtimestamp(limitReset/1000)

        msg = 'API rate limit '+name+' exceeded. Max '+str(requestCountLimit)+' calls in timewindow. Limit reset at '+limitResetDate.isoformat()+'.'
        
        #super().__init__(self, msg)
        #self.message = msg
        #self.limitResetDate = limitResetDate
        sys.exit(msg)
