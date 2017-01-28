"""Remove a dependency in the project.

.. code:: bash

   fdep rm <files...>
"""
import sys

from fdep.commands import ConfigRequiredMixin, SubcommandRunner


class RmCommandRunner(SubcommandRunner, ConfigRequiredMixin):
    """Handle rm commands."""
    COMMAND_NAME = 'rm'

    def run(self, *args, **kwargs):
        entry_names = {
            self.path_helper.resolve_path_to_entry(x)
            for x in args
        }
        for entry_name in entry_names:
            if self.entries.get(entry_name):
                del self.entries[entry_name]
            else:
                sys.stderr.write(self.messages.ERROR_NO_SUCH_FILE_IN_CONFIG.format(entry_name))
                return False
        self.config.save()

        for entry_name in entry_names:
            print(self.messages.REMOVED.format(entry_name))
        return True
