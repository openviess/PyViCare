# This decorator handles access to underlying JSON properties.
# If the property is not found (KeyError) or the index does not 
# exists (IndexError), the requested feature is not supported by 
# the device.
def handleNotSupported(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError):
        	raise PyViCareNotSupportedFeatureError(func.__name__)
    return wrapper

class PyViCareNotSupportedFeatureError(Exception):
    pass