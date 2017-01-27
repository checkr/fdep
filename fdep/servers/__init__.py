from abc import abstractmethod, ABCMeta


class RPCServer(object):
    """Implement an interface for servers."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def register_functions(self, func_pairs):
        pass

    @abstractmethod
    def serve_forever(self, **kwargs):
        pass
