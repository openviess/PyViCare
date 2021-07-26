import unittest
import os
import pytest
from PyViCare.PyViCare import PyViCare
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError

EXEC_INTEGRATION_TEST = int(os.getenv('EXEC_INTEGRATION_TEST', '0'))

def allGetterMethods(object):
    for method_name in dir(object):
        if method_name.startswith("get"):
            method = getattr(object, method_name)
            if callable(method):
                yield (method_name, method)

class Integration(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    @unittest.skipIf(not EXEC_INTEGRATION_TEST, "environments needed")
    def test_PyViCare(self):
        email = os.getenv('PYVICARE_EMAIL', '')
        password = os.getenv('PYVICARE_PASSWORD', '')
        client_id = os.getenv('PYVICARE_CLIENT_ID', '')

        vicare = PyViCare()
        vicare.initWithCredentials(email, password, client_id, "token.save")
        deviceConfig = vicare.devices[0]
        with self.capsys.disabled(): #allow print to showup in console
            print()
            print("model: %s" % deviceConfig.getModel())
            print("isOnline: %s" % deviceConfig.isOnline())

            device = deviceConfig.asGeneric()
            for (name, m) in allGetterMethods(device):
                try:
                    print("%s: %s" % (name, m()))
                except TypeError: #skip methods which have more than one argument
                    pass
                except PyViCareNotSupportedFeatureError:
                    print("%s: Not Supported" % name)

    
