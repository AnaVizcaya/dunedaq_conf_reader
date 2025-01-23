import pytest

def pytest_addoption(parser):
    parser.addoption("--branch-name", action="store", default="develop")
    parser.addoption("--repository", action="store", default="base")

@pytest.fixture
def branch_name(request):
    return request.config.option.branch_name

@pytest.fixture
def repository(request):

    if request.config.option.repository not in ["base", "operation"]:
        raise ValueError("Invalid repo name, should be either 'base' or 'operation'")

    return request.config.option.repository