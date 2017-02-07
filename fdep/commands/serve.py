"""Serve your model as a service.

.. code:: bash

   fdep serve [--driver=console] [--port=8181] <python module path>


Drivers
~~~~~~~

+---------+-----------------------------------------------------+--------------------------+
|Driver   | Description                                         | Options                  |
+=========+=====================================================+==========================+
| console | a simple command line interface for testing the     | ``--func=func_name``     |
|         | model locally.                                      |                          |
+---------+-----------------------------------------------------+--------------------------+
| xmlrpc  | a XMLRPC server driver.                             | ``--port=port``          |
|         |                                                     | ``--username``           |
|         |                                                     | ``--password``           |
|         |                                                     | ``--sentry_dsn``         |
|         |                                                     | ``--fluentd_http_url``   |
+---------+-----------------------------------------------------+--------------------------+
| jsonrpc | a JSONRPC server driver.                            | ``--port=port``          |
|         |                                                     | ``--username``           |
|         |                                                     | ``--password``           |
|         |                                                     | ``--sentry_dsn``         |
|         |                                                     | ``--fluentd_http_url``   |
+---------+-----------------------------------------------------+--------------------------+
"""
import os
import sys

from fdep.commands import ConfigRequiredMixin, SubcommandRunner
from fdep.servers.console import ConsoleServer
from fdep.servers.integrations.fluentd_http import FluentdHttpIntegration
from fdep.servers.integrations.sentry import SentryIntegration
from fdep.servers.jsonrpc import JSONRPCServer
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
        'jsonrpc': JSONRPCServer,
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
        username = kwargs.get('username') or os.environ.get('RPC_USERNAME')
        password = kwargs.get('password') or os.environ.get('RPC_PASSWORD')

        kwargs['port'] = port
        kwargs['username'] = username
        kwargs['password'] = password

        sentry_dsn = kwargs.get('sentry_dsn') or os.environ.get('SENTRY_DSN')
        sentry_integration = None
        if sentry_dsn:
            try:
                sentry_integration = SentryIntegration(sentry_dsn)
            except ImportError:
                sys.stderr.write(
                    self.messages.ERROR_NEED_TO_INSTALL_OPTIONAL.format('raven', 'Sentry')
                )

        try:
            # Ensure everything is installed safe and sound.
            if not self.root_runner.commands['install'].run():
                return False

            func_pairs = self.get_func_pairs(python_module_name)
            if server_driver_name in self.__class__.KNOWN_DRIVERS:
                server_driver = self.__class__.KNOWN_DRIVERS[server_driver_name]
            else:
                # User-provided driver
                server_driver_path, server_driver_class = server_driver_name.rsplit('.', 1)
                server_driver_module = self.resolve_module(server_driver_path)
                server_driver = getattr(server_driver_module, server_driver_class)

            integrations = []

            if sentry_integration is not None:
                integrations.append(sentry_integration)

            fluentd_http_url = kwargs.get('fluentd_http_url') or os.environ.get('FLUENTD_HTTP_URL')
            if fluentd_http_url:
                integrations.append(FluentdHttpIntegration(fluentd_http_url))

            if server_driver_name != 'console':
                print(self.messages.SERVING.format(server_driver_name, python_module_name, port))

            server = server_driver()
            server.register_integrations(integrations)
            server.register_functions(func_pairs)
            server.serve_forever(**kwargs)
        except Exception as e:
            if sentry_integration is not None:
                sentry_integration.capture_exception(e)
            raise
