import unittest
import os
import pytest
import json
from PyViCare.PyViCare import PyViCare
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError

EXEC_INTEGRATION_TEST = int(os.getenv('EXEC_INTEGRATION_TEST', '0'))


def allGetterMethods(object):
    for method_name in dir(object):
        if method_name.startswith("get"):
            method = getattr(object, method_name)
            if callable(method):
                yield (method_name, method)


def prettyPrintResults(result):
    # format dictionary and lists nicely
    if isinstance(result, dict) or isinstance(result, list):
        formatted = json.dumps(result, sort_keys=True, indent=2)
        indented = formatted.replace('\n', '\n' + ' ' * 45)
        return indented
    else:
        return result

def enablePrintStatementsForTest(test_case):
    return test_case.capsys.disabled()

class Integration(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    @unittest.skipIf(not EXEC_INTEGRATION_TEST, "environments needed")
    def test_PyViCare(self):
        email = os.getenv('PYVICARE_EMAIL', '')
        password = os.getenv('PYVICARE_PASSWORD', '')
        client_id = os.getenv('PYVICARE_CLIENT_ID', '')
        # method part defined on the PyViCareDeviceConfig type. e.g. as[value]() > asGeneric()
        expected_device_type = os.getenv('PYVICARE_DEVICE_TYPE', '')

        with enablePrintStatementsForTest(self):  
            print()

            vicare = PyViCare()
            vicare.initWithCredentials(
                email, password, client_id, "token.save")

            print("Found %s devices" % len(vicare.devices))

            for deviceConfig in vicare.devices:
                print()
                print(f"{'model':<45}{deviceConfig.getModel()}")
                print(f"{'isOnline':<45}{deviceConfig.isOnline()}")
                
                device = deviceConfig.asAutoDetectDevice()
                auto_type_name = type(device).__name__
                print(f"{'detected type':<45}{auto_type_name}")

                if expected_device_type != '':
                    self.assertEqual(auto_type_name, expected_device_type)
                
                for (name, method) in allGetterMethods(device):
                    result = None
                    try:
                        result = prettyPrintResults(method())
                    except TypeError:  # skip methods which have more than one argument
                        result = "Skipped"
                    except PyViCareNotSupportedFeatureError:
                        result = "Not Supported"
                    print(f"{name:<45}{result}")
            print()