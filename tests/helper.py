import json
import os
from datetime import datetime
from unittest.mock import patch

from PyViCare.PyViCareUtils import ViCareTimer


def readJson(fileName):
    test_filename = os.path.join(os.path.dirname(__file__), fileName)
    with open(test_filename, mode='rb') as json_file:
        return json.load(json_file)


def enablePrintStatementsForTest(test_case):
    return test_case.capsys.disabled()


def now_is(date_time):
    return patch.object(ViCareTimer, 'now', return_value=datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S'))
