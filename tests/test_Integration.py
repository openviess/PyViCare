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
    def test_PyViCare(self):
        email = os.getenv('PYVICARE_EMAIL', '')
        password = os.getenv('PYVICARE_PASSWORD', '')
        client_id = os.getenv('PYVICARE_CLIENT_ID', '')

        vicare = PyViCare()
        vicare.initWithCredentials(email, password, client_id, "token.save")
        deviceConfig = vicare.devices[0]
        with self.capsys.disabled(): #allow print to showup in console
            print()
            print(deviceConfig.getModel())
            print("Is online: %r" % deviceConfig.isOnline())

            device = deviceConfig.asGeneric()
            print("Outside temperature: %r" % device.getOutsideTemperature())
            print("Modes: %r" % device.getModes())