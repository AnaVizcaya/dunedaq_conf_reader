import pytest

def pytest_addoption(parser):
    parser.addoption("--branch-name", action="store", default="develop")
    parser.addoption("--repository", action="store", default="ssh://git@gitlab.cern.ch:7999/dune-daq/online/ehn1-daqconfigs.git")

@pytest.fixture
def branch_name(request):
    return request.config.option.branch_name

@pytest.fixture
def repository(request):
    return request.config.option.repository