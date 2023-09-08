'''
Setup Fixtures for Pytest
# https://docs.pytest.org/en/latest/reference/reference.html#command-line-flags
'''
import pytest
from modules import vectra

def pytest_addoption(parser):
    '''
    Define PyTest Options
    '''
    parser.addoption('--url', action='store', help='url or ip of vectra brain')
    parser.addoption('--user', help='username')
    parser.addoption('--password', help='password')
    parser.addoption('--token', help='token')


@pytest.fixture
def vc_v1(request):
    '''
    Define a v1 endpoint brain with a url, username, and password (deprecated)
    '''
    brain = request.config.getoption('--url')
    username = request.config.getoption('--user')
    passwd = request.config.getoption('--password')
    return vectra.VectraClient(url=brain, user=username, password=passwd)


@pytest.fixture
def vc_v2(request):
    '''
    Define a v2 endpoint brain with a url and token
    '''
    brain = request.config.getoption('--url')
    token = request.config.getoption('--token')
    return vectra.VectraClient(url=brain, token=token)


# def pytest_namespace():
#     return {'threatFeed': None}
