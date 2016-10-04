"""Interpret configuration files and execute."""
from fdep.config import FdepConfig
from fdep import __VERSION__
import requests
import boto3

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from textwrap import dedent
from colorama import Fore
from tqdm import tqdm
import sys
import os


class FdepInterpreter(object):

    def __init__(self, env, config_path, current_path='.'):
        self.env = env
        self.config_path = config_path
        self.current_path = current_path
        self.configure()

    def configure(self):
        try:
            self.base_dir = os.path.dirname(self.config_path)
            self.fdep = FdepConfig.load(self.config_path)
        except:
            self.base_dir = None
            self.fdep = None

    def initialize_project(self, *args):
        if self.fdep:
            sys.stderr.write(Fore.RED + 'Already initialized.\n' + Fore.RESET)
            return False

        if not len(args):
            args = [self.env]

        config_dict = {}
        for env in args:
            config_dict[env] = {}
        self.config_path = os.path.abspath(
            os.path.join(self.current_path, './fdep.yml'))
        self.fdep = FdepConfig(config_dict)
        self.fdep.save(self.config_path)
        self.configure()
        print('Initialized at {}'.format(self.config_path))
        return True

    def _install_one_dep(self, local_path, source):
        local_path = os.path.join(self.base_dir, local_path)

        try:
            os.makedirs(os.path.dirname(local_path))
        except:
            pass

        try:
            o = urlparse(source)
        except:
            sys.stderr.write(
                Fore.RED +
                '{} is an illegal URL.\n'.format(source) +
                Fore.RESET
            )
            return False

        if os.path.exists(local_path):
            print('[' + Fore.BLUE + '*' + Fore.RESET +
                  '] {} is already installed.'.format(local_path))
            return True

        print(
            ('[' + Fore.GREEN + '+' + Fore.RESET +
             '] Installing ' + Fore.BLUE + '{}' +
             Fore.RESET + ' from ' + Fore.RED + '{}' +
             Fore.RESET + '...').format(
                 local_path, source
            )
        )

        if o.scheme in ('http', 'https'):
            r = requests.get(source, stream=True)
            total_length = int(r.headers.get('content-length', 0))
            with open(local_path, 'wb') as f:
                with tqdm(total=total_length, unit='B', unit_scale=True) as pbar:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                        pbar.update(len(chunk))
        elif o.scheme in ('s3', ):
            bucket = o.netloc
            key = o.path[1:]
            client = boto3.client('s3')
            try:
                obj = client.get_object(Bucket=bucket, Key=key)
            except Exception as e:
                sys.stderr.write(
                    Fore.RED + 'AWS S3 Error: {}\n'.format(e) + Fore.RESET)
                return False
            total_length = obj.get('ContentLength', 0)
            with tqdm(total=total_length, unit='B', unit_scale=True) as pbar:
                client.download_file(
                    bucket, key, local_path, Callback=pbar.update)
        else:
            sys.stderr.write(
                Fore.RED +
                'Unsupported backend: {}\n'.format(o.scheme) +
                Fore.RESET
            )
            return False
        return True

    def _upload_one_dep(self, local_path):
        local_path = os.path.relpath(
            os.path.join(self.current_path, local_path),
            self.base_dir
        )

        try:
            source = self.fdep.config[self.env][local_path]
        except KeyError:
            sys.stderr.write(
                Fore.RED +
                "No such file in the fdep.yml: {}\n".format(local_path) +
                Fore.RESET
            )
            return False

        try:
            o = urlparse(source)
        except:
            sys.stderr.write(
                Fore.RED +
                '{} is an illegal URL.\n'.format(source) +
                Fore.RESET
            )
            return False

        print(
            ('[' + Fore.MAGENTA + '#' + Fore.RESET +
             '] Uploading ' + Fore.BLUE + '{}' +
             Fore.RESET + ' to ' + Fore.RED + '{}' +
             Fore.RESET + '...').format(
                 local_path, source
            )
        )

        if o.scheme in ('s3', ):
            bucket = o.netloc
            key = o.path[1:]
            client = boto3.client('s3')
            try:
                total_length = os.stat(
                    os.path.join(self.base_dir, local_path)
                ).st_size
            except:
                sys.stderr.write(
                    Fore.RED + 'File does not exist: {}\n'.format(local_path) + Fore.RESET)
                return False

            with tqdm(total=total_length, unit='B', unit_scale=True) as pbar:
                client.upload_file(local_path, bucket, key,
                                   Callback=pbar.update)
        else:
            sys.stderr.write(
                Fore.RED +
                'Unsupported backend: {}\n'.format(o.scheme) +
                Fore.RESET
            )
            return False
        return True

    def check(self):
        if self.fdep is None:
            sys.stderr.write(
                Fore.RED +
                "Missing fdep.yml. Please run fdep init first!\n" +
                Fore.RESET
            )
            return False

        if self.fdep.config.get(self.env) is None:
            sys.stderr.write(
                Fore.RED +
                "No section defined for the environment {}\n".format(
                    self.env) +
                Fore.RESET
            )
            return False
        return True

    def install_dependencies(self):
        for local_path, source in self.fdep.config[self.env].items():
            if not self._install_one_dep(local_path, source):
                sys.stderr.write(
                    Fore.RED +
                    "Error occurred while installing\n" +
                    Fore.RESET
                )
                return False
        return True

    def upload_dependencies(self, *local_paths):
        if not len(local_paths):
            sys.stderr.write(
                Fore.RED +
                'You have to manually specify which files to upload.\n' +
                Fore.RESET
            )
            return False

        for local_path in local_paths:
            if not self._upload_one_dep(local_path):
                sys.stderr.write(
                    Fore.RED +
                    "Error occurred while uploading\n" +
                    Fore.RESET
                )
                return False
        return True

    def add_dependency(self, alias, source):
        alias = os.path.join(self.current_path, alias)
        abs_alias = os.path.relpath(alias, self.base_dir)
        if self._install_one_dep(abs_alias, source):
            self.fdep.config[self.env][abs_alias] = source
            self.fdep.save(self.config_path)
            return True
        else:
            return False

    def rm_dependency(self, alias):
        alias = os.path.join(self.current_path, alias)
        abs_alias = os.path.relpath(alias, self.base_dir)
        del self.fdep.config[self.env][abs_alias]
        self.fdep.save(self.config_path)
        return True

    def print_usage(self):
        print(dedent("""\
        Usage: fdep <command> <arguments>

        fdep installs miscellaneous file dependencies. e.g. datasets, etc.

          help                            Print this helpful message
          version                         Print the currently installed version
          init <envs...>                  Create fdep.yml with specified environments
          install                         Install dependencies for the project
          upload <local path>             Upload a file to the storage
          add <local path> <remote path>  Add a new dependency to the project
          rm <local path>                 Remove a dependency in the project
        """))
        return True

    def print_version(self):
        print(__VERSION__)
        return True

    def run(self, argv):
        if not len(argv):
            self.print_usage()
            return False

        cmd = argv[0]
        args = argv[1:]

        print('[' + Fore.CYAN + '*' + Fore.RESET +
              '] Current environment: {}'.format(self.env))

        if cmd == 'init':
            return self.initialize_project(*args)
        elif cmd == 'install':
            if not self.check():
                return False
            return self.install_dependencies(*args)
        elif cmd == 'upload':
            if not self.check():
                return False
            return self.upload_dependencies(*args)
        elif cmd == 'add':
            if not self.check():
                return False
            return self.add_dependency(*args)
        elif cmd == 'rm':
            if not self.check():
                return False
            return self.rm_dependency(*args)
        elif cmd == 'help':
            return self.print_usage()
        elif cmd == 'version':
            return self.print_version()
        else:
            sys.stderr.write(
                Fore.RED + 'Unrecognized command: {}\n'.format(cmd) + Fore.RESET)
            self.print_usage()
            return False
