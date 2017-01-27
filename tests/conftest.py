import os
import shutil
import sys

from pytest import fixture

FIXTURE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures')


@fixture
def test_project_path(tmpdir_factory):
    return tmpdir_factory.mktemp('test_project', numbered=True).strpath


@fixture
def load_fixture(test_project_path):
    def _func(name_of_fixture):
        shutil.copytree(
            os.path.join(FIXTURE_PATH, name_of_fixture),
            os.path.join(test_project_path, 'project')
        )
    return _func


@fixture
def fdep(test_project_path):
    from fdep.__main__ import main

    def _func(*args):
        os.chdir(os.path.join(test_project_path, 'project'))
        return main(['fdep'] + list(args))
    return _func


@fixture
def load_config(test_project_path):
    from fdep.config import FdepConfig

    def _func():
        return FdepConfig.load(os.path.join(test_project_path, 'project', 'fdep.yml'))
    return _func


@fixture
def mock_requests_get(mocker):
    return mocker.patch('requests.get')


@fixture
def mock_s3(mocker):
    boto3_client = mocker.patch('boto3.client', autospec=True)
    s3_session = mocker.MagicMock(
        get_object=mocker.Mock(
            return_value={}
        )
    )
    boto3_client.return_value = s3_session
    return s3_session
