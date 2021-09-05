import json
import os


def readJson(fileName):
    test_filename = os.path.join(os.path.dirname(__file__), fileName)
    with open(test_filename, mode='rb') as json_file:
        return json.load(json_file)


def enablePrintStatementsForTest(test_case):
    return test_case.capsys.disabled()
