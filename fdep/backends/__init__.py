"""Define the backend interface."""
from abc import ABCMeta, abstractmethod
from fdep.utils import urlparse


class StorageBackend(object):
    """Define an abstract interface for backends."""

    __metaclass__ = ABCMeta
    BACKEND_REGISTRY = {}

    def __init__(self, interpreter, url):
        self.env = interpreter.env
        self.fdep = interpreter.fdep
        self.url = url
        self.interpreter = interpreter

    @classmethod
    def register(cls, scheme, klass):
        cls.BACKEND_REGISTRY[scheme] = klass

    @classmethod
    def create(cls, interpreter, url):
        o = urlparse(url)
        klass = cls.BACKEND_REGISTRY.get(o.scheme.lower())
        if klass:
            return o.scheme, klass(interpreter, url)
        else:
            return o.scheme, None

    @abstractmethod
    def get_to(self, local_path):
        pass

    @abstractmethod
    def put_from(self, local_path):
        pass
