"""Add a new file to the ``fdep.yml`` file.

.. code:: bash

   fdep add [--version=if_any] <local path> <remote path>

.. note:: This doesn't download the file. Use ``fdep install`` to download the files.
"""

import sys

from fdep.commands import ConfigRequiredMixin, SubcommandRunner


class AddCommandRunner(SubcommandRunner, ConfigRequiredMixin):
    """Handle add commands."""
    COMMAND_NAME = 'add'

    def run(self, *args, **kwargs):
        if len(args) != 2:
            sys.stderr.write(self.messages.ERROR_INVALID_ARGUMENT)
            self.root_runner.commands['help'].run()
            return False

        entry = self.path_helper.resolve_path_to_entry(args[0])
        source = args[1]

        self.entries[entry] = {"source": source}

        version = kwargs.get('version')

        if version:
            self.entries[entry]['version'] = version

        self.config.save()
        print(self.messages.ADDED.format(entry))
        return True
