def test_run_help(load_fixture, fdep):
    load_fixture('empty')
    assert fdep('help') == 0


def test_run_version(load_fixture, fdep):
    load_fixture('empty')
    assert fdep('version') == 0


def test_run_init(load_fixture, fdep):
    load_fixture('empty')
    assert fdep('init') == 0
    assert fdep('init') == 1  # Cannot initialize twice


def test_run_add(load_fixture, fdep):
    load_fixture('basic/http')
    assert fdep('add', 'run_add.txt', 'http://example.com/run_add.txt') == 0
    assert fdep('add', 'run_add.txt', 'http://example.com/run_add.txt') == 0  # Overwrite should work


def test_run_rm(load_fixture, fdep):
    load_fixture('basic/http')
    assert fdep('rm', 'data/wordlist.txt') == 0
    assert fdep('rm', 'data/wordlist.txt') == 1


def test_run_install_via_http(load_fixture, fdep, mock_requests_get):
    load_fixture('basic/http')
    assert fdep('install') == 0
    mock_requests_get.assert_called_with(
        'http://www-personal.umich.edu/~jlawler/wordlist', stream=True)

    mock_requests_get.reset_mock()
    assert fdep('install', 'data/wordlist.txt') == 0
    mock_requests_get.assert_not_called()  # For already downloaded files, it shouldn't redownload.


def test_run_install_via_s3(load_fixture, fdep, mock_s3):
    load_fixture('basic/s3')
    assert fdep('install') == 0
    mock_s3.get_object.assert_called_with(
        Bucket='ml-datasets', Key='wordlist.txt'
    )
    assert mock_s3.download_file.call_count > 0


def test_run_install_wrong_sha1sum(load_fixture, fdep, mock_s3):
    load_fixture('errors/sha1sum')
    assert fdep('install') == 1  # Already installed, but the sha1sum changed.
    mock_s3.get_object.assert_not_called()
    assert mock_s3.download_file.call_count == 0


def test_run_install_via_gspreadsheet(load_fixture, fdep, mock_requests_get):
    load_fixture('basic/gspreadsheet')
    assert fdep('install') == 0
    mock_requests_get.assert_called_with(
        'https://docs.google.com/spreadsheets/d/test-id/export?format=csv', stream=True)


def test_run_install_via_unsupported_backend(load_fixture, fdep):
    load_fixture('basic/unsupported')
    assert fdep('install') == 1


def test_run_upload_via_http(load_fixture, fdep):
    load_fixture('upload/http')
    assert fdep('upload', 'data/wordlist.txt') == 1


def test_run_upload_via_s3(load_fixture, fdep, mock_s3):
    load_fixture('upload/s3')
    assert fdep('upload', 'data/wordlist.txt') == 0
    assert mock_s3.upload_file.call_count > 0


def test_run_commit_via_s3(load_fixture, fdep, mock_s3, load_config):
    load_fixture('upload/s3')
    assert fdep('commit', 'data/wordlist.txt') == 0
    assert mock_s3.upload_file.call_count > 0
    assert load_config()['development']['data/wordlist.txt'].get('version') is not None


def test_run_upload_via_unsupported_backend(load_fixture, fdep):
    load_fixture('upload/unsupported')
    assert fdep('upload', 'data/wordlist.txt') == 1


def test_run_freeze_and_unfreeze(load_fixture, load_config, fdep):
    load_fixture('upload/http')
    assert fdep('freeze', 'data/wordlist.txt') == 0
    assert load_config()['development']['data/wordlist.txt'].get('sha1sum') is not None

    assert fdep('unfreeze', 'data/wordlist.txt') == 0
    assert load_config()['development']['data/wordlist.txt'].get('sha1sum') is None


def test_run_mv(load_fixture, load_config, fdep):
    load_fixture('basic/http')
    assert fdep('mv', 'data/wordlist.txt', 'data/test.txt') == 0
    assert load_config()['development'].get('data/wordlist.txt') is None
    assert load_config()['development'].get('data/test.txt') is not None


def test_run_link(load_fixture, load_config, fdep):
    load_fixture('basic/http')
    assert fdep('link', 'data/wordlist.txt', 'data/test.txt') == 0

    cfg = load_config()['development']
    o1 = cfg.get('data/wordlist.txt')
    o2 = cfg.get('data/test.txt')
    assert o1 == o2
