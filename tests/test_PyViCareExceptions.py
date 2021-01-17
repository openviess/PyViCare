import unittest
import datetime
from PyViCare.PyViCare import PyViCareRateLimitError, PyViCareRateLimitError
from tests.helper import readJson


class TestPyViCareRateLimitError(unittest.TestCase):

    def test_createFromResponse(self):
        mockResponse = readJson('response_rate_limit.json')

        error = PyViCareRateLimitError(mockResponse)

        self.assertEqual(error.message, 'API rate limit ViCare day limit exceeded. Max 1450 calls in timewindow. Limit reset at 2020-03-17T16:20:10.106000.')
        self.assertEqual(error.limitResetDate, datetime.datetime(2020, 3, 17, 16, 20, 10, 106000))


        

