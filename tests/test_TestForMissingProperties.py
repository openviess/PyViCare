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
            # general - not yet used
            'device.messages.info.raw',
            'device.messages.service.raw',
            'device.messages.status.raw',
            'device.parameterIdentification.version',
            'device.productIdentification',
            'device.productMatrix',
            'device.time.daylightSaving',
            'device.identification',
            'device.zigbee.parent.rx',
            'device.zigbee.parent.tx',
            'device.heatingCircuitId',
            'device.configuration.houseLocation',
            'device.lock.malfunction',
            'device.timeseries.burner.stops',
            'device.timeseries.dhw.burner.stops',
            'device.timeseries.ignitionTimeSteps',
            'device.timeseries.monitoringIonization',
            'device.timeseries.water.pressure.peaks',
            'device.information',
            'device.configuration.measurementWeight',
            'device.configuration.houseLocation',
            'device.lock.malfunction',
            'device.timeseries.burner.stops',
            'device.timeseries.dhw.burner.stops',
            'device.timeseries.ignitionTimeSteps',
            'device.timeseries.monitoringIonization',
            'device.timeseries.water.pressure.peaks',
            'device.zigbee.active',
            'device.zigbee.status',
            'device.actorSensorTest',
            'device.brand',
            'device.lock.external',
            'device.power.consumption.limitation',
            'device.power.statusReport.consumption',
            'device.power.statusReport.production',
            'device.type',
            'device.variant',
            'heating.boiler.pumps.internal.current',
            'heating.boiler.temperature.current',
            'heating.compressors.0.heater.crankcase',
            'heating.compressors.0.sensors.pressure.inlet',
            'heating.compressors.0.sensors.temperature.inlet',
            'heating.compressors.0.sensors.temperature.motorChamber',
            'heating.compressors.0.sensors.temperature.oil',
            'heating.compressors.0.sensors.temperature.outlet',
            'heating.compressors.0.speed.current',
            'heating.condensors.0.sensors.temperature.liquid',
            'heating.configuration.heatingRod.dhw',
            'heating.configuration.heatingRod.heating',
            'heating.configuration.internalPumpOne',
            'heating.configuration.internalPumpTwo',
            'heating.configuration.temperature.outside.DampingFactor',
            'heating.economizers.0.sensors.temperature.liquid',
            'heating.evaporators.0.heater.base',
            'heating.evaporators.0.sensors.temperature.liquid',
            'heating.evaporators.0.sensors.temperature.overheat',
            'heating.external.lock',
            'heating.heat.production.summary.cooling',
            'heating.heater.condensatePan',
            'heating.heater.fanRing',
            'heating.heatingRod',
            'heating.inverters.0.sensors.power.current',
            'heating.inverters.0.sensors.power.output',
            'heating.inverters.0.sensors.temperature.powerModule',
            'heating.outdoor.defrosting',
            'heating.power.consumption.summary.cooling',
            'heating.primaryCircuit.fans.0.current',
            'heating.primaryCircuit.valves.fourThreeWay',
            'heating.secondaryCircuit.operation.state',
            'heating.secondaryCircuit.temperature.return.minimum',
            'heating.secondaryCircuit.valves.fourThreeWay',
            'heating.secondaryHeatGenerator',
            'heating.valves.fourThreeWay.position',
            'tcu.wifi',

            'heating.boiler.pumps.internal',
            'heating.boiler.pumps.internal.target',
            'heating.burners.0.demand.temperature',
            'heating.calculated.temperature.outside',
            'heating.circuits.0.configuration.summerEco.absolute',
            'heating.configuration.bufferCylinderSize',
            'heating.configuration.centralHeatingCylinderSize',
            'heating.configuration.dhwCylinderPump',
            'heating.configuration.dhwCylinderSize',
            'device.messages.info.raw',
            'heating.configuration.gasType',
            'heating.configuration.houseHeatingLoad',
            'heating.configuration.houseLocation',
            'heating.configuration.houseOrientation',
            'heating.configuration.internalPumps',
            'heating.configuration.pressure.total',
            'heating.dhw.scaldProtection',
            'heating.heat.production.summary.dhw',
            'heating.heat.production.summary.heating',

            # heating ignored for now
            'heating.operating.programs.holidayAtHome',
            'heating.operating.programs.holiday',
            'heating.device.time.offset',
            'heating.configuration.multiFamilyHouse',
            'heating.boiler.airflaps.0.position.current',
            'heating.boiler.airflaps.1.position.current',
            'heating.boiler.pumps.internal',
            'heating.boiler.pumps.internal.target',

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
            'heating.sensors.temperature.allengra',

            'heating.dhw.operating.modes.active',
            'heating.dhw.operating.modes.comfort',
            'heating.dhw.operating.modes.eco',

            'heating.circuits.0.heating.roomInfluenceFactor',
            'heating.circuits.0.temperature',  # TODO: to analyse, from Vitodens 100W
            'heating.circuits.0.operating.programs.noDemand.hmiState',  # TODO: to analyse, from Vitodens 100W
            'heating.circuits.0.name',  # TODO: to analyse, from Vitodens 100W
            'heating.circuits.0.zone.mode',  # TODO: to analyse, from Vitocal 250A

            'heating.configuration.dhw.temperature.dhwCylinder.max',  # TODO: to analyse, from Vitocal 333G

            'heating.buffer.sensors.temperature.main',  # deprecated, removed 2024-09-15 FIXME: remove once data point is removed and test data is updated
            'heating.buffer.sensors.temperature.top',  # deprecated, removed 2024-09-15 FIXME: remove once data point is removed and test data is updated
            'heating.dhw.sensors.temperature.hotWaterStorage',  # deprecated, removed 2024-09-15 FIXME: remove once data point is removed and test data is updated
            'heating.dhw.sensors.temperature.hotWaterStorage.top',  # deprecated, removed 2024-09-15 FIXME: remove once data point is removed and test data is updated
            'heating.dhw.sensors.temperature.hotWaterStorage.bottom',  # deprecated, removed 2024-09-15 FIXME: remove once data point is removed and test data is updated
            'heating.burner', # deprecated FIXME: remove once test data is updated

            # Ignored for now as they are not documented in https://documentation.viessmann.com/static/iot/data-points
            'heating.device.variant',
            'heating.device.software',

            # gateway

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
            'heating.heatingRod.power.consumption.summary.dhw',
            'heating.heatingRod.power.consumption.summary.heating',
            'heating.heatingRod.status',
            'heating.power.consumption.current',
            'heating.scop.dhw', # deprecated
            'heating.scop.heating', # deprecated
            'heating.scop.total', # deprecated
            'heating.dhw.comfort', # deprecated

            'rooms.others', # TODO: No idea what it is yet
            'rooms.status', # TODO: No idea what it is yet

            # energy system - not yet used
            'device.etn',
            'device.serial.internalComponents',
            'ess.battery.usedAverage',
            'ess.configuration.backupBox',
            'ess.configuration.systemType',
            'ess.inverter.ac.power',
            'ess.sensors.temperature.ambient',
            'ess.version.hardware',
            'heating.device.mainECU',
            'pcc.ac.active.current',
            'pcc.ac.active.power',
            'pcc.ac.reactive.power',
            'pcc.state.gridCode',
            'photovoltaic.installedPeakPower',
            'photovoltaic.string.current',
            'photovoltaic.string.voltage',

            # TRVs
            'device.zigbee.lqi',
            'device.zigbee.parent.id',
            'trv.childLock',
            'trv.mountingMode',
            'trv.valve.position',

            # FHT
            'fht.configuration.floorCoolingCondensationShutdownMargin',
            'fht.configuration.floorCoolingCondensationThreshold',
            'fht.configuration.floorHeatingDamageProtectionThreshold',
            'fht.valve',
        ]

        all_features = self.read_all_features()
        all_python_files = self.read_all_python_code()

        missing_features = {}
        for feature in all_features:
            found = self.find_feature_in_code(all_python_files, feature)

            foundInFiles = all_features[feature]['files']
            if not found and len(foundInFiles) > 0 and feature not in ignore:
                missing_features[feature] = foundInFiles

        self.maxDiff = None
        self.assertDictEqual({}, missing_features, "found new data points")

    def test_unverifiedProperties(self):
        # with this test we want to verify if we access
        # properties which are not in any test response data

        ignore = [
            'heating.dhw.sensors.temperature.dhwCylinder.midBottom',  # FIXME: remove once test data is updated
            'ventilation.quickmodes',
            'heating.heatingRod.heat.production.current',
            'heating.heatingRod.power.consumption.current',
            'heating.heatingRod.power.consumption.heating',
            'heating.heatingRod.power.consumption.dhw',
            'heating.heatingRod.power.consumption.total',
            'heating.compressors.0.power.consumption.current',
            'heating.compressors.0.power.consumption.heating',
            'heating.compressors.0.heat.production.current',
            'heating.compressors.0.power.consumption.cooling',
            'heating.compressors.0.power.consumption.dhw',
            'heating.compressors.0.power.consumption.total',
        ]

        all_features = self.read_all_features()
        all_python_files = self.read_all_python_code()

        used_features = []
        for python in all_python_files:
            if python in ['PyViCareFuelCell.py']:  # skip, where we miss test data
                continue

            for match in re.findall(r'getProperty\(\s*?f?"(.*)"\s*?\)', all_python_files[python]):
                feature_name = re.sub(r'{self.(circuit|burner|compressor|room)}', '0', match)
                feature_name = re.sub(r'{burner}', '0', feature_name)
                feature_name = re.sub(r'\.{(quickmode|mode|program|active_program)}', '', feature_name)
                used_features.append(feature_name)

        self.maxDiff = None
        self.assertSetEqual(set([]), set(used_features) - set(all_features) - set(ignore), "found untested data points")

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
