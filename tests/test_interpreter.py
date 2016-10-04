from fdep.interpreter import FdepInterpreter
from fdep.config import FdepConfig


def test_run_help(fdep_yml):
    ipt = FdepInterpreter('default', fdep_yml)
    assert ipt.run(['help'])


def test_run_version(fdep_yml):
    ipt = FdepInterpreter('default', fdep_yml)
    assert ipt.run(['version'])


def test_run_init(test_project_path, empty_fdep_yml):
    ipt = FdepInterpreter('default', None, current_path=test_project_path)
    assert ipt.run(['init'])

    with open(empty_fdep_yml) as f:
        assert f.read() == 'default: {}\n'


def test_run_add(fdep_yml, test_project_path, mocker):
    requests_get = mocker.patch('requests.get')

    ipt = FdepInterpreter('default', fdep_yml, current_path=test_project_path)
    assert ipt.run(['add', 'run_add.txt', 'http://example.com/run_add.txt'])
    assert ipt.fdep.config['default'].get('run_add.txt') is not None
    requests_get.assert_called_with(
        'http://example.com/run_add.txt', stream=True)

    reloaded_fdep = FdepConfig.load(fdep_yml)
    assert reloaded_fdep.config['default'].get('run_add.txt') is not None


def test_run_rm(fdep_yml, test_project_path):
    ipt = FdepInterpreter('default', fdep_yml, current_path=test_project_path)
    assert ipt.run(['rm', 'data/wordlist.txt'])
    assert ipt.fdep.config['default'].get('data/wordlist.txt') is None

    reloaded_fdep = FdepConfig.load(fdep_yml)
    assert reloaded_fdep.config['default'].get('data/wordlist.txt') is None


def test_run_install_via_http(fdep_yml, test_project_path, mocker):
    requests_get = mocker.patch('requests.get')

    ipt = FdepInterpreter('default', fdep_yml, current_path=test_project_path)
    assert ipt.run(['install'])

    requests_get.assert_called_with(
        'http://www-personal.umich.edu/~jlawler/wordlist', stream=True)


def test_run_install_via_s3(fdep_yml, test_project_path, mocker):
    boto3_client = mocker.patch('boto3.client', autospec=True)
    s3_session = mocker.MagicMock(
        get_object=mocker.Mock(
            return_value={}
        )
    )
    boto3_client.return_value = s3_session

    ipt = FdepInterpreter('production', fdep_yml,
                          current_path=test_project_path)
    assert ipt.run(['install'])
    s3_session.get_object.assert_called_with(
        Bucket='my-ml-project', Key='modified-wordlist.txt'
    )
    assert s3_session.download_file.call_count > 0


def test_run_install_via_unsupported_backend(fdep_yml, test_project_path):
    ipt = FdepInterpreter('unsupported', fdep_yml,
                          current_path=test_project_path)
    assert not ipt.run(['install'])


def test_run_upload_via_http(fdep_yml, test_project_path):
    ipt = FdepInterpreter('default', fdep_yml, current_path=test_project_path)
    assert not ipt.run(['upload', 'data/wordlist.txt'])


def test_run_upload_via_s3(fdep_yml, test_project_path, wordlist_txt, mocker):
    boto3_client = mocker.patch('boto3.client', autospec=True)
    s3_session = mocker.MagicMock()
    boto3_client.return_value = s3_session

    ipt = FdepInterpreter('production', fdep_yml,
                          current_path=test_project_path)
    assert ipt.run(['upload', 'data/wordlist.txt'])
    assert s3_session.upload_file.call_count > 0


def test_run_upload_via_unsupported_backend(fdep_yml, test_project_path):
    ipt = FdepInterpreter('unsupported', fdep_yml,
                          current_path=test_project_path)
    assert not ipt.run(['upload', 'data/wordlist.txt'])
