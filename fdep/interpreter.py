"""Interpret configuration files and execute."""
import binascii
import os
import sys
from hashlib import sha1

from fdep import __VERSION__, messages
from fdep.backends import StorageBackend
from fdep.backends.http import HTTPBackend
from fdep.backends.s3 import S3Backend
from fdep.backends.gspreadsheet import GSpreadsheetBackend
from fdep.config import FdepConfig
from tqdm import tqdm


class FdepInterpreter(object):

    def __init__(self, env, config_path, current_path='.'):
        self.messages = messages.FdepDefaultMessages
        self.env = env
        self.config_path = config_path
        self.current_path = current_path
        self.configure()

    def configure(self):
        """Configure the current object with the initial arguments."""
        try:
            self.base_dir = os.path.dirname(self.config_path)
            self.fdep = FdepConfig.load(self.config_path)
        except:
            self.base_dir = None
            self.fdep = None

    def start_progress(self, length):
        """Set up the progress bar.

        This is a callback function from the storage backend.
        """
        if sys.version_info.major <= 2:
            use_ascii = True
        else:
            use_ascii = False

        self.pbar = tqdm(
            total=length, unit='B', unit_scale=True, ascii=use_ascii)

    def progress_callback(self, length):
        """Update the progress bar's progress.

        This is a callback function from the storage backend.
        """
        self.pbar.update(length)

    def end_progress(self):
        """Clean up the progress bar.

        This is a callback function from the storage backend.
        """
        self.pbar.close()

    def initialize_project(self, *args):
        """Initialize a project.

        You can run this by `fdep init`.
        """
        if self.fdep:
            sys.stderr.write(self.messages.ALREADY_INITIALIZED)
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
        print(self.messages.INITIALIZED.format(self.config_path))
        return True

    def get_sha1sum(self, path):
        """Return a hexdigested SHA1 sum for the file path."""
        if not os.path.exists(path):
            return None

        with open(path, 'rb') as f:
            m = sha1()
            m.update(f.read())
        return m.hexdigest()

    def get_real_local_path(self, local_path):
        """Get the real path of an input local path."""
        return os.path.join(self.base_dir, local_path)

    def create_directory(self, path):
        """Create directories until the path recursively."""
        try:
            os.makedirs(path)
            return True
        except:
            return False

    def get_source_from_config(self, local_path):
        """Get a URL that matches the local path in the configuration file."""
        try:
            env = self.fdep.config[self.env]
        except KeyError:
            sys.stderr.write(
                self.messages.ERROR_NO_SUCH_SECTION_DEFINED.format(self.env))
            return

        try:
            if isinstance(env[local_path], str):
                return env[local_path], None
            else:
                return env[local_path]['source'], env[local_path].get('sha1sum')
        except KeyError:
            sys.stderr.write(
                self.messages.ERROR_NO_SUCH_FILE_IN_CONFIG.format(local_path))

    def try_running_backend(self, backend_bag, func):
        """Attempt to run appropriate methods in backend."""
        b_type, backend = backend_bag
        if backend:
            try:
                func(backend)
            except Exception as e:
                sys.stderr.write(self.messages.ERROR_OTHER.format(e))
                return False
        else:
            sys.stderr.write(
                self.messages.ERROR_UNSUPPORTED_BACKEND.format(b_type))
            return False
        return True

    def install_dependency(self, local_path, source, sha1sum=None, version=None):
        """Install one dependency."""
        local_path, alias = self.get_real_local_path(local_path), local_path
        self.create_directory(os.path.dirname(local_path))
        source_to_use = source

        if version:
            source_to_use += '_{}'.format(version)

        if os.path.exists(local_path):
            new_sha1sum = self.get_sha1sum(local_path)
            if sha1sum is not None and sha1sum != new_sha1sum:
                print(self.messages.FILE_CHANGED.format(local_path))
            else:
                print(self.messages.ALREADY_INSTALLED.format(local_path))
            return True

        print(self.messages.INSTALLING.format(local_path, source_to_use))

        backend_bag = StorageBackend.create(self, source_to_use)
        result = self.try_running_backend(
            backend_bag, lambda backend: backend.get_to(local_path))

        new_sha1sum = self.get_sha1sum(self.get_real_local_path(local_path))
        if sha1sum is not None and sha1sum != new_sha1sum:
            sys.stderr.write(
                self.messages.ERROR_WRONG_SHA1SUM.format(sha1sum, new_sha1sum))
            return False
        elif sha1sum is None:
            self.fdep.config[self.env][alias] = {
                'source': source,
                'sha1sum': new_sha1sum
            }
            if version:
                self.fdep.config[self.env][alias]['version'] = version
            self.fdep.save(self.config_path)
        return result

    def upload_dependency(self, local_path, versioning=False):
        """Upload one dependency."""
        local_path = os.path.relpath(
            os.path.join(self.current_path, local_path),
            self.base_dir
        )
        real_local_path = self.get_real_local_path(local_path)
        source, sha1sum = self.get_source_from_config(local_path)
        new_sha1sum = self.get_sha1sum(real_local_path)
        source_to_use = source

        if versioning:
            version = binascii.hexlify(os.urandom(16)).decode()
            source_to_use += '_{}'.format(version)

        if not os.path.exists(real_local_path):
            sys.stderr.write(
                self.messages.ERROR_NO_SUCH_FILE_ON_DISK.format(real_local_path))
            return False

        print(self.messages.UPLOADING.format(local_path, source_to_use))

        backend_bag = StorageBackend.create(self, source_to_use)
        result = self.try_running_backend(
            backend_bag, lambda backend: backend.put_from(real_local_path))

        if result:
            self.fdep.config[self.env][local_path] = {
                'source': source,
                'sha1sum': new_sha1sum
            }
            if versioning:
                self.fdep.config[self.env][local_path]['version'] = version
                print(self.messages.NEW_VERSION_UPLOADED.format(version, local_path))
            self.fdep.save(self.config_path)
        return result

    def check(self):
        """Check if the configuration file is valid."""
        if self.fdep is None:
            sys.stderr.write(self.messages.ERROR_MISSING_FDEP)
            return False

        if self.fdep.config.get(self.env) is None:
            sys.stderr.write(
                self.messages.ERROR_NO_SUCH_SECTION_DEFINED.format(self.env))
            return False
        return True

    def install_dependencies(self):
        """Install dependencies specified in the configuration file.

        This can be invoked by `fdep install`.
        """
        for local_path, source_obj in self.fdep.config[self.env].items():
            if not isinstance(source_obj, str):
                # New format with sha1sum
                sha1sum = source_obj.get('sha1sum')
                version = source_obj.get('version')
                source = source_obj.get('source')
            else:
                source = source_obj
                sha1sum = None
                version = None

            if not self.install_dependency(local_path, source, version=version, sha1sum=sha1sum):
                sys.stderr.write(self.messages.ERROR_WHILE_INSTALLING)
                return False

        return True

    def upload_dependencies(self, *local_paths, **kwargs):
        """Upload dependencies specified in the configuration file.

        This can be invoked by `fdep upload`.
        """
        versioning = kwargs.get('versioning')

        if not len(local_paths):
            sys.stderr.write(self.messages.ERROR_NO_FILES_TO_UPLOAD)
            return False

        for local_path in local_paths:
            if not self.upload_dependency(local_path, versioning=versioning):
                sys.stderr.write(self.messages.ERROR_WHILE_UPLOADING)
                return False
        return True

    def add_dependency(self, alias, source, version=None):
        """Add a new dependency to the configuration file.

        This can be invoked by `fdep add`.
        """
        alias = os.path.join(self.current_path, alias)
        abs_alias = os.path.relpath(alias, self.base_dir)
        if self.install_dependency(abs_alias, source):
            self.fdep.config[self.env][alias] = {
                'source': source,
                'sha1sum': self.get_sha1sum(abs_alias)
            }
            if version:
                self.fdep.config[self.env][alias]['version'] = version
            self.fdep.save(self.config_path)
            return True
        else:
            return False

    def rm_dependency(self, alias):
        """Remove a dependency from the configuration file.

        This can be invoked by `fdep rm`.
        """
        alias = os.path.join(self.current_path, alias)
        abs_alias = os.path.relpath(alias, self.base_dir)
        del self.fdep.config[self.env][abs_alias]
        self.fdep.save(self.config_path)
        return True

    def print_usage(self):
        """Print the usage.

        This can be invoked by `fdep help`.
        """
        print(self.messages.USAGE)
        return True

    def print_version(self):
        """Print the version of fdep.

        This can be invoked by `fdep version`.
        """
        print(__VERSION__)
        return True

    def run(self, argv):  # noqa
        """Interpret the argv and run appropriate methods."""
        if not len(argv):
            self.print_usage()
            return False

        cmd, args = argv[0], argv[1:]

        print(self.messages.CURRENT_ENVIRONMENT.format(self.env))

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
        elif cmd == 'commit':
            if not self.check():
                return False
            return self.upload_dependencies(*args, versioning=True)
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
            sys.stderr.write(self.messages.UNRECOGNIZED_COMMAND.format(cmd))
            self.print_usage()
            return False
