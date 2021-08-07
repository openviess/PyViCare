# Feature flag to raise an exception in case of a non existing device feature.
# The flag should be fully removed in a later release.
# It allows dependend libraries to gracefully migrate to the new behaviour
raise_exception_on_not_supported_device_feature = True

# Feature flag to raise exception if rate limit of the API is hit
raise_exception_on_rate_limit = True

# Feature flag to raise exception on command calls if the API does not return (2xx or 3xx) responses.
raise_exception_on_command_failure = True
