# Feature flag to raise an exception in case of a non existing device feature.
# The flag should be fully removed in a later release. 
# It allows dependend libraries to gracefully migrate to the new behaviour
raise_exception_instead_of_returning_error = False