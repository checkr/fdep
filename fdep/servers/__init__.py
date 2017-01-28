from abc import abstractmethod, ABCMeta


class RPCServer(object):
    """Implement an interface for RPC servers."""
    __metaclass__ = ABCMeta

    def __init__(self):
        self.integrations = []

    def register_integrations(self, integrations):
        self.integrations = integrations

    @abstractmethod
    def register_functions(self, func_pairs):
        """Register functions for the server.

        :param list func_pairs: A list of tuples (function_name, function)
        """
        pass

    @abstractmethod
    def serve_forever(self, **kwargs):
        """Serve forever.

        :param int port: A port number
        """
        pass

    def wrap_function(self, name, func):
        """Wrap a function before it gets registered.

        This hooks up the integrations.
        """
        def _func(*args, **kwargs):
            # before_function
            for integration in self.integrations:
                integration.before_function(name, args, kwargs)

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                for integration in self.integrations:
                    integration.capture_exception(e)
                raise

            # after_function
            for integration in self.integrations:
                integration.after_function(name, args, kwargs, result)

            return result
        return _func
