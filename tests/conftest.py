from pytest import fixture
from textwrap import dedent
import os


@fixture
def test_project_path(tmpdir_factory):
    return tmpdir_factory.mktemp('test_project', numbered=True).strpath


@fixture
def empty_fdep_yml(test_project_path):
    return os.path.join(test_project_path, 'fdep.yml')


@fixture
def fdep_yml(empty_fdep_yml):
    with open(empty_fdep_yml, 'w') as f:
        f.write(dedent("""\
        default:
          data/wordlist.txt: http://www-personal.umich.edu/~jlawler/wordlist
        production:
          data/wordlist.txt: s3://my-ml-project/modified-wordlist.txt
        unsupported:
          data/wordlist.txt: unsupported://test.txt
        """))
    return empty_fdep_yml


@fixture
def data_directory(test_project_path):
    path = os.path.join(test_project_path, 'data')
    os.mkdir(path)
    return path


@fixture
def wordlist_txt(data_directory):
    path = os.path.join(data_directory, 'wordlist.txt')
    with open(path, 'w') as f:
        f.write('hello\nworld\n')
    return path
