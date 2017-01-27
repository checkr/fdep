import os
import sys

from fdep.commands import ConfigRequiredMixin, SubcommandRunner
from fdep.servers.console import ConsoleServer
from fdep.servers.integrations.fluentd_http import FluentdHttpIntegration
from fdep.servers.integrations.sentry import SentryIntegration
from fdep.servers.xmlrpc import XMLRPCServer


class ServeCommandRunner(SubcommandRunner, ConfigRequiredMixin):
    """Handle serve commands.

    Users can also bring their own server implementation.
    """
    COMMAND_NAME = 'serve'
    DEFAULT_PORT = 8181
    DEFAULT_DRIVER = 'console'
    KNOWN_DRIVERS = {
        'console': ConsoleServer,
        'xmlrpc': XMLRPCServer,
    }

    def resolve_module(self, module_name):
        try:
            sys.path.append('.')
            module = __import__(module_name)

            names_to_resolve = module_name.split('.')[1:]
            for name in names_to_resolve:
                module = getattr(module, name)
        except ImportError:
            sys.stderr.write(self.messages.ERROR_NO_SUCH_MODULE.format(module_name))
            return None
        return module

    def get_func_pairs(self, module_name):
        module = self.resolve_module(module_name)
        if module is None:
            return []

        pairs = []
        for name in dir(module):
            candidate = getattr(module, name)
            if callable(candidate):
                pairs.append((name, candidate))
        return pairs

    def run(self, *args, **kwargs):
        if len(args) != 1:
            sys.stderr.write(self.messages.ERROR_INVALID_ARGUMENT)
            self.root_runner.commands['help'].run()
            return False

        python_module_name = args[0]
        port = kwargs.get('port') or os.environ.get('PORT') or self.__class__.DEFAULT_PORT
        server_driver_name = kwargs.get('driver') or\
            os.environ.get('SERVER_DRIVER') or self.__class__.DEFAULT_DRIVER

        kwargs['port'] = port

        # Ensure everything is installed safe and sound.
        if not self.root_runner.commands['install'].run():
            return False

        func_pairs = self.get_func_pairs(python_module_name)
        if server_driver_name in self.__class__.KNOWN_DRIVERS:
            server_driver = self.__class__.KNOWN_DRIVERS[server_driver_name]
        else:
            # User-provided driver
            server_driver = self.resolve_module(server_driver_name)

        integrations = []
        # TODO

        if server_driver_name != 'console':
            print(self.messages.SERVING.format(server_driver_name, python_module_name, port))

        server = server_driver()
        server.register_functions(func_pairs)
        server.serve_forever(**kwargs)