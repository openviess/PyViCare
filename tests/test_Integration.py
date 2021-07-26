import unittest
import os
import pytest
from PyViCare.PyViCare import PyViCare

EXEC_INTEGRATION_TEST = int(os.getenv('EXEC_INTEGRATION_TEST', '0'))

class Integration(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    @unittest.skipIf(not EXEC_INTEGRATION_TEST, "environments needed")
    def test_impl(self):
        vicare = PyViCare()
        email = os.getenv('PYVICARE_EMAIL', '')
        password = os.getenv('PYVICARE_PASSWORD', '')
        client_id = os.getenv('PYVICARE_CLIENT_ID', '')
        vicare.initWithCredentials(email, password, client_id, "token.save")
        device = vicare.devices[0]

        with self.capsys.disabled(): 
            print()
            print(device.getModel())