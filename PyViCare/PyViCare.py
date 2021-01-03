import PyViCare.Feature

# This decorator handles access to underlying JSON properties.
# If the property is not found (KeyError) or the index does not 
# exists (IndexError), the requested feature is not supported by 
# the device.
def handleNotSupported(func):
    def wrapper(*args, **kwargs):
        try:
            try:
                return func(*args, **kwargs)
            except (KeyError, IndexError):
                raise PyViCareNotSupportedFeatureError(func.__name__)
        except PyViCareNotSupportedFeatureError:
            if PyViCare.Feature.raise_exception_instead_of_returning_error:
                raise
            else:
                return "error"
    return wrapper

class PyViCareNotSupportedFeatureError(Exception):
    pass