"""Print local and recent versions.

.. code:: bash

   fdep version
"""
import pkg_resources
import requests
from fdep import __VERSION__
from fdep.commands import SubcommandRunner


class VersionCommandRunner(SubcommandRunner):
    """Handle version commands."""
    COMMAND_NAME = 'version'
    PYPI_REGISTRY_API_URL = 'http://pypi.python.org/pypi/fdep/json'

    def run(self):
        local_version = __VERSION__
        remote_version = None

        try:
            remote_version = requests.get(self.__class__.PYPI_REGISTRY_API_URL)\
                            .json()['info']['version']
        except:
            remote_version = 'NETWORK ERROR'

        print(self.messages.FDEP_LOCAL_VERSION.format(local_version))
        print(self.messages.FDEP_RECENT_VERSION.format(remote_version))

        if pkg_resources.parse_version(remote_version) > \
                pkg_resources.parse_version(local_version):
            print(self.messages.FDEP_NEW_VERSION_EXISTS)
        return True
