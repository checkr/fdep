"""Upload the file with a version tag.

.. code:: bash

   fdep commit [--version=custom_version_tag] <files...>

.. note:: This adds `version` in the entry in the ``fdep.yml`` file.
"""
import sys

from fdep.commands import ConfigRequiredMixin, SubcommandRunner
from fdep.utils import HashHelper


class CommitCommandRunner(SubcommandRunner, ConfigRequiredMixin):
    """Handle commit commands."""
    COMMAND_NAME = 'commit'

    def run(self, *args, **kwargs):
        if not len(args):
            sys.stderr.write(self.messages.ERROR_NO_FILES_TO_UPLOAD)
            self.root_runner.commands['help'].run()
            return False

        new_version = kwargs.get('version', HashHelper.generate_random_hash())

        paths = {self.path_helper.resolve_path_to_entry(x) for x in args}
        entries = [(y, self.entries.get(y)) for y in paths]

        for entry_name, entry in entries:
            if entry is None:
                sys.stderr.write(self.messages.ERROR_NO_SUCH_FILE_IN_CONFIG.format(entry_name))
                return False
            entry['version'] = new_version
            self.entries[entry_name] = entry

        self.root_runner.commands['upload'].run(*[x[0] for x in entries])

        for entry_name, entry in entries:
            print(self.messages.NEW_VERSION_UPLOADED.format(new_version, entry_name))
        self.config.save()
        return True
