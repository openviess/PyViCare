import json
import re
import unittest
from os import listdir
from os.path import dirname, isfile, join

import pytest

from tests.helper import readJson


class TestForMissingProperties(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    def test_missingProperties(self):

        ignore = [
            'heating.operating.programs.holidayAtHome',
            'heating.operating.programs.holiday',
            'heating.device.time.offset',
            'heating.configuration.multiFamilyHouse',
            'heating.boiler.temperature',  # ignore as value is to low to be plausible in response data

            'heating.circuits.0.dhw.pumps.circulation.schedule',
            'heating.circuits.0.dhw.schedule',
            'heating.power.consumption.dhw',

            'heating.circuits.0.temperature.levels',  # hint: command
            'heating.dhw.temperature.hysteresis',  # hint: command
        ]

        all_features = self.read_all_features()
        all_python_files = self.read_all_python_code()

        missing_features = {}
        for feature in all_features:
            found = self.find_feature_in_code(all_python_files, feature)

            foundInFiles = all_features[feature]['files']
            if not found and len(foundInFiles) > 0 and feature not in ignore:
                missing_features[feature] = foundInFiles

        has_missing_features = len(missing_features) > 0
        self.assertFalse(has_missing_features, json.dumps(missing_features, sort_keys=True, indent=2))

    def find_feature_in_code(self, all_python_files, feature):
        search_string = f'[\'"]{feature}[\'"]'.replace(".", r"\.")
        search_string = re.sub(r"\b\d\b", r"{.*?}", search_string)
        search_string = re.sub(r'\\.modes\\.\w+', r'\\.modes\\.\\w+', search_string)
        search_string = re.sub(r'\\.programs\\.\w+', r'\\.programs\\.\\w+', search_string)

        found = False
        for search_python in all_python_files:
            if re.search(search_string, all_python_files[search_python]):
                found = True
                break
        return found

    def read_all_python_code(self):
        python_path = join(dirname(__file__), '../PyViCare')
        python_files = [f for f in listdir(python_path) if isfile(join(python_path, f))]

        all_python_files = {}

        for python in python_files:
            with open(join(python_path, python)) as f:
                all_python_files[python] = f.read()
        return all_python_files

    def read_all_features(self):
        response_path = join(dirname(__file__), './response')
        response_files = [f for f in listdir(response_path) if isfile(join(response_path, f))]

        all_features = {}
        for response in response_files:
            data = readJson(join(response_path, response))
            if "data" in data:
                for feature in data["data"]:
                    name = re.sub(r"\b\d\b", "0", feature["feature"])
                    if name not in all_features:
                        all_features[name] = {'files': []}

                    if feature['isEnabled'] and feature['properties'] != {} and feature['components'] == []:
                        all_features[name]['files'].append(response)
        return all_features
