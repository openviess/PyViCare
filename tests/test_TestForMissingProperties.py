import re
import unittest
from os import listdir
from os.path import dirname, isdir, isfile, join

from tests.helper import readJson


class PythonFile:
    def __init__(self, filename, path):
        self.filename = filename
        self.path = path


class TestForMissingProperties(unittest.TestCase):
    def test_missingProperties(self):
        # with this test we want to check if new properties
        # are added to the response files

        ignore = [
            'heating.operating.programs.holidayAtHome',
            'heating.operating.programs.holiday',
            'heating.device.time.offset',
            'heating.configuration.multiFamilyHouse',
            'heating.boiler.temperature',  # ignore as value is to low to be plausible in response data
            'heating.boiler.airflaps.0.position.current',
            'heating.boiler.airflaps.1.position.current',

            'heating.circuits.0.dhw.pumps.circulation.schedule',
            'heating.circuits.0.dhw.schedule',
            'heating.power.consumption.dhw',
            'heating.power.consumption',

            'heating.circuits.0.temperature.levels',  # hint: command
            'heating.dhw.hygiene',
            'heating.dhw.temperature',
            'heating.burners',

            'heating.dhw.hygiene.trigger',
            'heating.dhw.operating.modes.off',
            'heating.dhw.temperature.hygiene',
            'heating.power.production.cumulative',
            'heating.power.purchase.cumulative',
            'heating.power.purchase.current',
            'heating.power.sold.cumulative',
            'heating.power.sold.current',
            'heating.sensors.temperature.allengra',

            'heating.dhw.operating.modes.active',
            'heating.dhw.operating.modes.comfort',
            'heating.dhw.operating.modes.eco',

            'heating.circuits.0.heating.roomInfluenceFactor',
            'heating.circuits.0.temperature',  # TODO: to analyse, from Vitodens 100W
            'heating.circuits.0.operating.programs.noDemand.hmiState',  # TODO: to analyse, from Vitodens 100W
            'heating.circuits.0.name',  # TODO: to analyse, from Vitodens 100W
            'heating.circuits.0.zone.mode',  # TODO: to analyse, from Vitocal 250A
            'heating.dhw.sensors.temperature.dhwCylinder',

            'heating.configuration.dhw.temperature.dhwCylinder.max',  # TODO: to analyse, from Vitocal 333G

            'heating.buffer.sensors.temperature.main',  # deprecated, removed 2024-09-15 FIXME: remove once data point is removed and test data is updated
            'heating.buffer.sensors.temperature.top',  # deprecated, removed 2024-09-15 FIXME: remove once data point is removed and test data is updated
            'heating.dhw.sensors.temperature.hotWaterStorage',  # deprecated, removed 2024-09-15 FIXME: remove once data point is removed and test data is updated
            'heating.dhw.sensors.temperature.hotWaterStorage.top',  # deprecated, removed 2024-09-15 FIXME: remove once data point is removed and test data is updated
            'heating.dhw.sensors.temperature.hotWaterStorage.bottom',  # deprecated, removed 2024-09-15 FIXME: remove once data point is removed and test data is updated
            'heating.burner', # deprecated FIXME: remove once test data is updated

            # Ignored for now as they are not documented in https://documentation.viessmann.com/static/iot/data-points
            'device.messages.errors.raw',
            'device.name',
            'device.power.battery',
            'device.productIdentification',
            'device.productMatrix',
            'heating.device.variant',
            'device.time.daylightSaving',
            'heating.device.software',

            # gateway
            'gateway.devices',  # not used

            # ventilation - not yet used
            'ventilation.levels.levelOne',
            'ventilation.levels.levelTwo',
            'ventilation.levels.levelThree',
            'ventilation.levels.levelFour',
            'ventilation.quickmodes.forcedLevelFour', # quickmode accessible via getVentilationQuickmode
            'ventilation.quickmodes.silent',
            'ventilation.quickmodes.standby',
            'ventilation.quickmodes.comfort',
            'ventilation.quickmodes.eco',
            'ventilation.quickmodes.holiday',
            'ventilation.operating.state',  # TODO: to analyse, from Vitocal 111S
            'heating.heatingRod.power.consumption.summary.dhw',
            'heating.heatingRod.power.consumption.summary.heating',
            'heating.heatingRod.status',
            'heating.power.consumption.current',
            'heating.scop.dhw', # deprecated
            'heating.scop.heating', # deprecated
            'heating.scop.total', # deprecated
            'heating.dhw.comfort', # deprecated
        ]

        all_features = self.read_all_features()
        all_python_files = self.read_all_python_code()

        missing_features = {}
        for feature in all_features:
            found = self.find_feature_in_code(all_python_files, feature)

            foundInFiles = all_features[feature]['files']
            if not found and len(foundInFiles) > 0 and feature not in ignore:
                missing_features[feature] = foundInFiles

        self.assertDictEqual({}, missing_features)

    def test_unverifiedProperties(self):
        # with this test we want to verify if we access
        # properties which are not in any test response data

        ignore = [
            'heating.dhw.sensors.temperature.dhwCylinder.midBottom',  # FIXME: remove once test data is updated
            'ventilation.quickmodes',
        ]

        all_features = self.read_all_features()
        all_python_files = self.read_all_python_code()

        used_features = []
        for python in all_python_files:
            if python in ['PyViCareFuelCell.py']:  # skip, where we miss test data
                continue

            for match in re.findall(r'getProperty\(\s*?f?"(.*)"\s*?\)', all_python_files[python]):
                feature_name = re.sub(r'{self.(circuit|burner|compressor)}', '0', match)
                feature_name = re.sub(r'{burner}', '0', feature_name)
                feature_name = re.sub(r'\.{(quickmode|mode|program|active_program)}', '', feature_name)
                used_features.append(feature_name)

        self.assertSetEqual(set([]), set(used_features) - set(all_features) - set(ignore))

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
        # searches in all subdirectories
        python_files = self.get_all_files(python_path)

        all_python_files = {}

        for python in python_files:
            if not python.filename.endswith(".py"):
                continue

            with open(join(python.path, python.filename)) as f:
                all_python_files[python.filename] = f.read()

        return all_python_files

    def get_all_files(self, path):
        files = []
        for f in listdir(path):
            new_path = join(path, f)
            if isdir(new_path):
                files.extend(self.get_all_files(new_path))
            elif isfile(new_path):
                files.append(PythonFile(f, path))

        return files

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

                    if feature['isEnabled'] and feature['properties'] != {}:
                        all_features[name]['files'].append(response)
        return all_features
