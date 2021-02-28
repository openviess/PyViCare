import pytest
from tests.ViCareServiceMock import ViCareServiceMock
from PyViCare.PyViCareFuelCell import FuelCell
from PyViCare.PyViCareGazBoiler import GazBoiler
import inspect

@pytest.fixture
def service():
    return ViCareServiceMock('response_VitovalorPT2.json', 0)

@pytest.fixture
def fuelcell(service):
    return FuelCell(None, None, None, 0, 0, service)

def get_fields(clazz):
    return [name for name, _ in inspect.getmembers(clazz, predicate=inspect.isfunction)
        if name.startswith('get')]

def get_fuelcell_fields():
    return sorted(list(set(get_fields(FuelCell)) - set(get_fields(GazBoiler))))

@pytest.mark.parametrize("field", get_fuelcell_fields())
def test_field(fuelcell, field):
    # call method
    getattr(fuelcell, field)()
