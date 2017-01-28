"""Freeze a file with a SHA1SUM.

.. code:: bash

   fdep freeze <files...>

Once you freeze a file, fdep will check the file's sha1sum every download, to make sure your model is always reproducible.
"""
import os
import sys

from fdep.commands import ConfigRequiredMixin, SubcommandRunner
from fdep.utils import HashHelper


class FreezeCommandRunner(SubcommandRunner, ConfigRequiredMixin):
    """Handle freeze commands."""
    COMMAND_NAME = 'freeze'

    def run(self, *args, **kwargs):
        if not len(args):
            sys.stderr.write(self.messages.ERROR_INVALID_ARGUMENT)
            self.root_runner.commands['help'].run()
            return False

        entry_names = {self.path_helper.resolve_path_to_entry(path) for path in args}

        frozen_entries = []
        for entry_name in entry_names:
            path = self.path_helper.resolve_entry_to_path(entry_name)
            entry = self.entries.get(entry_name)

            if entry is None:
                sys.stderr.write(self.messages.ERROR_NO_SUCH_FILE_IN_CONFIG.format(entry_name))
                return False
            if not os.path.exists(path):
                sys.stderr.write(self.messages.ERROR_NO_SUCH_FILE_ON_DISK.format(path))
                return False

            sha1sum = HashHelper.calculate_sha1sum(path)
            entry['sha1sum'] = sha1sum

            self.entries[entry_name] = entry
            frozen_entries.append(entry_name)
        self.config.save()

        for entry_name in frozen_entries:
            print(self.messages.FROZEN.format(entry_name))

        return True
