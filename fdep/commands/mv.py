"""Rename a dependency in the project.

.. code:: bash

   fdep mv <file 1> <file 2>
"""
import sys

from fdep.commands import ConfigRequiredMixin, SubcommandRunner


class MvCommandRunner(SubcommandRunner, ConfigRequiredMixin):
    """Handle mv commands."""
    COMMAND_NAME = 'mv'

    def run(self, *args, **kwargs):
        if len(args) != 2:
            sys.stderr.write(self.messages.ERROR_INVALID_ARGUMENT)
            self.root_runner.commands['help'].run()
            return False

        entry_name1 = self.path_helper.resolve_path_to_entry(args[0])
        entry_name2 = self.path_helper.resolve_path_to_entry(args[1])

        if not self.entries.get(entry_name1):
            sys.stderr.write(self.messages.ERROR_NO_SUCH_FILE_IN_CONFIG.format(entry_name1))
            return False

        self.entries[entry_name2] = self.entries[entry_name1]
        del self.entries[entry_name1]

        print(self.messages.RENAMED.format(entry_name1, entry_name2))
        self.config.save()
        return True
