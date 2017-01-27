"""Define the backend interface."""
from abc import ABCMeta, abstractmethod
from fdep.utils import urlparse
import sys


class StorageBackend(object):
    """Define an abstract interface for backends."""
    __metaclass__ = ABCMeta

    def __init__(self, root_runner, progressbar, url):
        self.root_runner = root_runner
        self.progressbar = progressbar
        self.url = url

    @classmethod
    def _create(cls, root_runner, progressbar, url):
        o = urlparse(url)
        klass = root_runner.backends.get(o.scheme.lower())
        if klass:
            return o.scheme, klass(root_runner, progressbar, url)
        else:
            return o.scheme, None

    @classmethod
    def execute(cls, root_runner, progressbar, url, func_name, *args):
        """Try running a backend function.

        It returns whether it was successfull and which backend it ran.
        """
        b_type, backend = cls._create(root_runner, progressbar, url)
        if backend:
            try:
                getattr(backend, func_name)(*args)
            except Exception as e:
                sys.stderr.write(root_runner.messages.ERROR_OTHER.format(e))
                return False, b_type
        else:
            sys.stderr.write(
                root_runner.messages.ERROR_UNSUPPORTED_BACKEND.format(b_type))
            return False, b_type
        return True, b_type

    @abstractmethod
    def get_to(self, local_path):
        pass

    @abstractmethod
    def put_from(self, local_path):
        pass
