import json
import os
import unittest

import pytest

from PyViCare.PyViCare import PyViCare
from PyViCare.PyViCareUtils import PyViCareNotSupportedFeatureError
from tests.helper import enablePrintStatementsForTest

EXEC_INTEGRATION_TEST = int(os.getenv('EXEC_INTEGRATION_TEST', '0'))
TOKEN_FILE = "browser.save"


def all_getter_methods(obj):
    for method_name in dir(obj):
        if method_name.startswith("get"):
            method = getattr(obj, method_name)
            if callable(method):
                yield (method_name, method)


def pretty_print_results(result):
    # format dictionary and lists nicely
    if isinstance(result, dict) or isinstance(result, list):
        formatted = json.dumps(result, sort_keys=True, indent=2)
        indented = formatted.replace('\n', '\n' + ' ' * 45)
        return indented
    else:
        return result


def dump_results(vicare_device):
    for (name, method) in all_getter_methods(vicare_device):
        result = None
        try:
            result = pretty_print_results(method())
        except TypeError:  # skip methods which have more than one argument
            result = "Skipped"
        except PyViCareNotSupportedFeatureError:
            result = "Not Supported"
        print(f"{name:<45}{result}")


def create_client():
    client_id = os.getenv('PYVICARE_CLIENT_ID', '')

    vicare = PyViCare()
    vicare.initWithBrowserOAuth(client_id, TOKEN_FILE)
    return vicare


class Integration(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    @unittest.skipIf(not EXEC_INTEGRATION_TEST, "environments needed")
    def test_PyViCare(self):
        with enablePrintStatementsForTest(self):
            print()

            vicare = create_client()

            print(f"Found {len(vicare.devices)} devices")

            for device_config in vicare.devices:
                print()
                print(f"{'model':<45}{device_config.getModel()}")
                print(f"{'isOnline':<45}{device_config.isOnline()}")

                device = device_config.asAutoDetectDevice()
                auto_type_name = type(device).__name__
                print(f"{'detected type':<45}{auto_type_name}")

                print(f"{'Roles':<45}{', '.join(device.service.roles)})")

                dump_results(device)
                print()

                for circuit in device.circuits:
                    print(f"{'Use circuit':<45}{circuit.id}")
                    dump_results(circuit)
                    print()

                for burner in device.burners:
                    print(f"{'Use burner':<45}{burner.id}")
                    dump_results(burner)
                    print()

                for compressor in device.compressors:
                    print(f"{'Use compressor':<45}{compressor.id}")
                    dump_results(compressor)
                    print()

            print()

            for i in vicare.installations:
                print(i.id)
                print(i.description)
                print(i.address.street)
                print()
                for g in i.gateways:
                    print(g.producedAt)
                    print(g.autoUpdate)
                    print(g.aggregatedStatus)
                    print(g.registeredAt)
                    print()
                    for d in g.devices:
                        print(d.modelId)
                        print(d.createdAt)

    @unittest.skipIf(not EXEC_INTEGRATION_TEST, "environments needed")
    def test_dump(self):
        with enablePrintStatementsForTest(self):
            vicare = vicare = create_client()

            with open("dump.json", mode='w', encoding="utf-8") as output:
                output.write(vicare.devices[0].dump_secure())

            with open("dump.flat.json", mode='w', encoding="utf-8") as output:
                output.write(vicare.devices[0].dump_secure(flat=True))
