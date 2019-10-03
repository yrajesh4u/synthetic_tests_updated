import pytest
from pytest_lib import config

@pytest.fixture(scope="session")
def generate_mind_url():
    """
    This fixture generates the middle mind url by using data from the current yaml file
    """
    return config["mindHost"] + ":" + config["mindPort"] + "/" + config["mindService"]

@pytest.fixture(scope="session")
def generate_json_headers():
    """
    This fixture generates default headers used by mind guide requests which use json as content type.
    """
    return {'Accept': 'application/json', 'X-Middlemind-RequestId': "true", 'Content-Type': 'application/json'}