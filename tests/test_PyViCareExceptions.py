import datetime
import unittest

from PyViCare.PyViCareUtils import PyViCareCommandError, PyViCareRateLimitError
from tests.helper import readJson


class TestPyViCareRateLimitError(unittest.TestCase):

    def test_createFromResponse(self):
        mockResponse = readJson('response/rate_limit.json')

        error = PyViCareRateLimitError(mockResponse)

        self.assertEqual(
            error.message, 'API rate limit ViCare day limit exceeded. Max 1450 calls in timewindow. Limit reset at 2020-03-17T16:20:10.106000.')
        self.assertEqual(error.limitResetDate, datetime.datetime(
            2020, 3, 17, 16, 20, 10, 106000))


class TestPyViCareCommandError(unittest.TestCase):

    def test_createFromResponse(self):
        mockResponse = readJson('response/error_502.json')

        error = PyViCareCommandError(mockResponse)

        self.assertEqual(
            error.message, 'Command failed with status code 502. Reason given was: INTERNAL_SERVER_ERROR')
