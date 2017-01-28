"""Initialize a new fdep project.

.. code:: bash

   fdep init [<envs...>]

.. note:: If ``envs`` were not given, it'll default to ``development``.
"""
from fdep.commands import SubcommandRunner
from fdep.config import FdepConfig


class InitCommandRunner(SubcommandRunner):
    """Handle init commands."""
    COMMAND_NAME = 'init'

    def validate(self):
        if self.config:
            raise Exception(self.messages.ALREADY_INITIALIZED)

    def run(self, *args, **kwargs):
        if not len(args):
            envs = {self.env}
        else:
            envs = set(args)

        config_dict = {}
        for env in envs:
            config_dict[env] = {}

        FdepConfig(self.root_path, config_dict).save()
        print(self.messages.INITIALIZED.format(self.root_path))
        return True
