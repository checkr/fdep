"""Interpret configuration files and execute."""
import sys

from fdep import messages
from fdep.backends.gspreadsheet import GSpreadsheetBackend
from fdep.backends.http import HTTPBackend, HTTPSBackend
from fdep.backends.s3 import S3Backend
from fdep.commands import CommandRunner
from fdep.commands.add import AddCommandRunner
from fdep.commands.commit import CommitCommandRunner
from fdep.commands.freeze import FreezeCommandRunner
from fdep.commands.help import HelpCommandRunner
from fdep.commands.init import InitCommandRunner
from fdep.commands.install import InstallCommandRunner
from fdep.commands.link import LinkCommandRunner
from fdep.commands.mv import MvCommandRunner
from fdep.commands.rm import RmCommandRunner
from fdep.commands.serve import ServeCommandRunner
from fdep.commands.unfreeze import UnfreezeCommandRunner
from fdep.commands.upload import UploadCommandRunner
from fdep.commands.version import VersionCommandRunner
from fdep.utils import PathHelper


class FdepRunner(CommandRunner):
    """Implement the root runner.

    This manages subcommand runners and runs them with the proper context.
    """
    AVAILABLE_COMMANDS = [
        HelpCommandRunner,
        VersionCommandRunner,
        AddCommandRunner,
        InstallCommandRunner,
        UnfreezeCommandRunner,
        FreezeCommandRunner,
        InitCommandRunner,
        MvCommandRunner,
        RmCommandRunner,
        CommitCommandRunner,
        UploadCommandRunner,
        LinkCommandRunner,
        ServeCommandRunner,
    ]
    AVAILABLE_BACKENDS = [
        HTTPBackend,
        HTTPSBackend,
        S3Backend,
        GSpreadsheetBackend,
    ]

    def __init__(self, env, config):
        self.env = env
        self.config = config
        self.path_helper = PathHelper(env, config)
        self.messages = messages.FdepDefaultMessages

        # Build tables
        self.commands = {klass.COMMAND_NAME: klass(self) for klass in self.__class__.AVAILABLE_COMMANDS}
        self.backends = {klass.SCHEME_NAME: klass for klass in self.__class__.AVAILABLE_BACKENDS}

    def run(self, *args, **kwargs):
        """Interpret the argv and run appropriate methods."""
        args = list(args)
        print(self.messages.CURRENT_ENVIRONMENT.format(self.env))
        if not len(args):
            cmd = command = None
        else:
            cmd = args.pop(0)
            command = self.commands.get(cmd)

        if not command:
            if cmd:
                sys.stderr.write(self.messages.UNRECOGNIZED_COMMAND.format(cmd))
            command = self.commands['help']
        return command.validate_and_run(*args, **kwargs)
