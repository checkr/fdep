"""Unfreeze a file.

.. code:: bash

   fdep unfreeze <files...>

It removes the SHA1SUM for a file in the ``fdep.yml`` file.
"""

import sys

from fdep.commands import ConfigRequiredMixin, SubcommandRunner


class UnfreezeCommandRunner(SubcommandRunner, ConfigRequiredMixin):
    """Handle unfreeze commands."""
    COMMAND_NAME = 'unfreeze'

    def run(self, *args, **kwargs):
        if not len(args):
            sys.stderr.write(self.messages.ERROR_INVALID_ARGUMENT)
            self.root_runner.commands['help'].run()
            return False

        entry_names = {self.path_helper.resolve_path_to_entry(path) for path in args}

        unfrozen_entries = []
        for entry_name in entry_names:
            path = self.path_helper.resolve_entry_to_path(entry_name)
            entry = self.entries.get(entry_name)

            if entry is None:
                sys.stderr.write(self.messages.ERROR_NO_SUCH_FILE_IN_CONFIG.format(entry_name))
                return False

            if entry.get('sha1sum'):
                del entry['sha1sum']

            self.entries[entry_name] = entry
            unfrozen_entries.append(entry_name)
        self.config.save()

        for entry_name in unfrozen_entries:
            print(self.messages.UNFROZEN.format(entry_name))

        return True
