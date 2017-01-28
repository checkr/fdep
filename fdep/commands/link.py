"""Link two entries in the ``fdep.yml`` file.

.. code:: bash

   fdep link [env:]<file> [env:]<file>

By doing this, you can have the same configuration in two different environments.
"""
import sys

from fdep.commands import ConfigRequiredMixin, SubcommandRunner


class LinkCommandRunner(SubcommandRunner, ConfigRequiredMixin):
    """Handle link commands."""
    COMMAND_NAME = 'link'

    def run(self, *args, **kwargs):
        if len(args) != 2:
            sys.stderr.write(self.messages.ERROR_INVALID_ARGUMENT)
            self.root_runner.commands['help'].run()
            return False

        to_link = list(args)

        if ':' in to_link[0]:
            env1, to_link[0] = to_link[0].split(':', 1)
            if not self.config.get(env1):
                sys.stderr.write(self.messages.ERROR_NO_SUCH_SECTION_DEFINED.format(env1))
                return False
        else:
            env1 = self.env

        if ':' in to_link[1]:
            env2, to_link[1] = to_link[1].split(':', 1)
            if not self.config.get(env2):
                sys.stderr.write(self.messages.ERROR_NO_SUCH_SECTION_DEFINED.format(env2))
                return False
        else:
            env2 = self.env

        entry_name1 = self.path_helper.resolve_path_to_entry(to_link[0])
        entry_name2 = self.path_helper.resolve_path_to_entry(to_link[1])

        if not self.config[env1].get(entry_name1):
            sys.stderr.write(self.messages.ERROR_NO_SUCH_FILE_IN_CONFIG.format(entry_name1))
            return False

        self.config[env2][entry_name2] = self.config[env1][entry_name1]

        print(self.messages.LINKED.format(*args))
        self.config.save()
        return True
