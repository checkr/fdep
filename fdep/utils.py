"""Implement miscellaneous utilties. e.g. urlparse, etc."""
import binascii
import errno
import os
from hashlib import sha1

try:
    from urlparse import urlparse
except ImportError:  # pragma: no cover
    from urllib.parse import urlparse


class PathHelper(object):
    """Implement helpful methods to resolve paths and names based on the context.

    The context is given by the root command runner and the instnace itself resides inside it.
    """

    def __init__(self, env, config):
        self.env = env
        self.config = config

    def resolve_entry_to_path(self, entry_name, current_path=None):
        """Resolve an entry name to an actual path.

        If `current_path` wasn't given, it'll use the root path.
        """
        if current_path is None:
            current_path = self.config.root_path
        current_path = os.path.abspath(current_path)
        return os.path.join(current_path, entry_name)

    def resolve_path_to_entry(self, path, current_path=None):
        """Resolve a relative/absolute path to an entry name in the configuration file.

        If `current_path` wasn't given, it'll use the root path.
        """
        if current_path is None:
            current_path = self.config.root_path
        current_path = os.path.abspath(current_path)
        return os.path.relpath(path, current_path)

    def ensure_directories(self, path):
        """Create directories until the path can be happy when created.

        Basically the same as `mkdir -p path`
        """
        try:
            return os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


class HashHelper(object):
    """Implement helpful methods to generate random hashes and calculate sha1sum.

    Context is not needed for this class.
    """

    @classmethod
    def generate_random_hash(cls, size=16):
        return binascii.hexlify(os.urandom(size)).decode()

    @classmethod
    def calculate_sha1sum(cls, path):
        if not os.path.exists(path):
            return None

        with open(path, 'rb') as f:
            m = sha1()
            m.update(f.read())
        return m.hexdigest()
