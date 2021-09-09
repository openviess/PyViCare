from datetime import datetime, timedelta
from functools import wraps
from typing import Callable

from PyViCare import Feature

# This decorator handles access to underlying JSON properties.
# If the property is not found (KeyError) or the index does not
# exists (IndexError), the requested feature is not supported by
# the device.


def time_as_delta(date_time: datetime) -> timedelta:
    return timedelta(
        hours=date_time.hour,
        minutes=date_time.minute,
        seconds=date_time.second
    )


def parse_time_as_delta(time_string: str) -> timedelta:
    return timedelta(
        hours=int(time_string[0:2]),
        minutes=int(time_string[3:5])
    )


class ViCareTimer:
    # class is used to replace logic in unittest
    def now(self) -> datetime:
        return datetime.now()


def handleNotSupported(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, IndexError):
            raise PyViCareNotSupportedFeatureError(func.__name__)

    # You can remove that wrapper after the feature flag gets removed entirely.
    def feature_flag_wrapper(*args, **kwargs):
        try:
            return wrapper(*args, **kwargs)
        except PyViCareNotSupportedFeatureError:
            if Feature.raise_exception_on_not_supported_device_feature:
                raise
            else:
                return "error"
    return feature_flag_wrapper


def handleAPICommandErrors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, IndexError):
            raise PyViCareCommandError(func.__name__)

    # You can remove that wrapper after the feature flag gets removed entirely.
    def feature_flag_wrapper(*args, **kwargs):
        try:
            return wrapper(*args, **kwargs)
        except PyViCareCommandError:
            if Feature.raise_exception_on_command_failure:
                raise
            else:
                return "error"
    return feature_flag_wrapper


class PyViCareNotSupportedFeatureError(Exception):
    pass


class PyViCareInvalidCredentialsError(Exception):
    pass


class PyViCareBrowserOAuthTimeoutReachedError(Exception):
    pass


class PyViCareInvalidDataError(Exception):
    pass


class PyViCareRateLimitError(Exception):

    def __init__(self, response):
        extended_payload = response["extendedPayload"]
        name = extended_payload["name"]
        requestCountLimit = extended_payload["requestCountLimit"]
        limitReset = extended_payload["limitReset"]
        limitResetDate = datetime.utcfromtimestamp(limitReset / 1000)

        msg = f'API rate limit {name} exceeded. Max {requestCountLimit} calls in timewindow. Limit reset at {limitResetDate.isoformat()}.'

        super().__init__(self, msg)
        self.message = msg
        self.limitResetDate = limitResetDate


class PyViCareInternalServerError(Exception):
    def __init__(self, response):
        statusCode = response["statusCode"]

        message = response["message"]
        viErrorId = response["viErrorId"]

        msg = f'Request failed with status code {statusCode} and message "{message}". ViCare ErrorId: {viErrorId}'

        super().__init__(self, msg)
        self.message = msg


class PyViCareCommandError(Exception):
    def __init__(self, response):
        statusCode = response["statusCode"]

        extended_payload = response["extendedPayload"]
        reason = extended_payload["reason"]

        msg = f'Command failed with status code {statusCode}. Reason given was: {reason}'

        super().__init__(self, msg)
        self.message = msg
