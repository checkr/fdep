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

    def __init__(self, env, config_path):
        self.env = env
        self.config_path = config_path
        self.base_dir = os.path.dirname(config_path)
        self.fdep = FdepConfig.load(config_path)

    def _install_one_dep(self, local_path, source):
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
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
            print('[' + Fore.BLUE + '*' + Fore.RESET + '] {} is already installed.'.format(local_path))
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
                sys.stderr.write(Fore.RED + 'AWS S3 Error: {}\n'.format(e) + Fore.RESET)
                return False
            total_length = obj.get('ContentLength', 0)
            with tqdm(total=total_length, unit='B', unit_scale=True) as pbar:
                client.download_file(bucket, key, local_path, Callback=pbar.update)
        else:
            sys.stderr.write(
                Fore.RED +
                'Unsupported backend: {}\n'.format(o.scheme) +
                Fore.RESET
            )
            return False
        return True

    def _upload_one_dep(self, local_path):
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
                total_length = os.stat(local_path).st_size
            except:
                sys.stderr.write(Fore.RED + 'File does not exist: {}\n'.format(local_path) + Fore.RESET)
                return False
            
            with tqdm(total=total_length, unit='B', unit_scale=True) as pbar:
                client.upload_file(local_path, bucket, key, Callback=pbar.update)
        else:
            sys.stderr.write(
                Fore.RED +
                'Unsupported backend: {}\n'.format(o.scheme) +
                Fore.RESET
            )
            return False
        return True
    
    def check(self):
        if not self.fdep.config.get(self.env):
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
        abs_alias = os.path.relpath(alias, self.base_dir)
        if self._install_one_dep(abs_alias, source):
            self.fdep.save(self.config_path)
        else:
            return False

    def rm_dependency(self, alias):
        abs_alias = os.path.relpath(alias, self.base_dir)
        del self.fdep.config[self.env][abs_alias]
        self.fdep.save(self.config_path)

    def print_usage(self):
        print(dedent("""\
        Usage: fdep <command> <arguments>

        fdep installs miscellaneous file dependencies. e.g. datasets, etc.

          help                            Print this helpful message
          version                         Print the currently installed version
          install                         Install dependencies for the project
          upload <local path>             Upload a file to the storage
          add <local path> <remote path>  Add a new dependency to the project
          rm <local path>                 Remove a dependency in the project
        """))

    def print_version(self):
        print(__VERSION__)

    def run(self, argv):
        if not len(argv):
            self.print_usage()
            return False

        cmd = argv[0]
        args = argv[1:]

        # Configuration validity check
        if not self.check():
            return False

        print('[' + Fore.CYAN + '*' + Fore.RESET + '] Current environment: {}'.format(self.env))

        if cmd == 'install':
            return self.install_dependencies(*args)
        elif cmd == 'upload':
            return self.upload_dependencies(*args)
        elif cmd == 'add':
            return self.add_dependency(*args)
        elif cmd == 'rm':
            return self.rm_dependency(*args)
        elif cmd == 'help':
            return self.print_usage()
        elif cmd == 'version':
            return self.print_version()
        else:
            sys.stderr.write(Fore.RED + 'Unrecognized command: {}\n'.format(cmd) + Fore.RESET)
            self.print_usage()
            return False
