"""Define a command runner interface.

A interface for each command was needed to avoid intermangled
within the interpreter logic.
"""
from abc import ABCMeta, abstractmethod
import sys
import os


class CommandRunner(object):
    """Define an interface for command runners.

    Comamnd runners include the root runner, and also subcommands.
    """
    __metaclass__ = ABCMeta

    @property
    def root_path(self):
        if self.config:
            return self.config.root_path
        else:
            return os.getcwd()

    @property
    def entries(self):
        return self.config[self.env]

    def validate_and_run(self, *args, **kwargs):
        try:
            if getattr(self, 'validate', None):
                self.validate()
        except Exception as e:
            sys.stderr.write(str(e))
            return False
        return self.run(*args, **kwargs)


class ConfigRequiredMixin(object):
    """Implement a mixin for CommandRunner."""

    def validate(self):
        if self.config is None:
            raise Exception(self.messages.ERROR_MISSING_FDEP)

        if self.config.get(self.env) is None:
            raise Exception(
                self.messages.ERROR_NO_SUCH_SECTION_DEFINED.format(self.env))


class SubcommandRunner(CommandRunner):
    """Implement a shortcut class for subcommands."""

    def __init__(self, root_runner):
        self.root_runner = root_runner

    @property
    def config(self):
        return self.root_runner.config

    @property
    def path_helper(self):
        return self.root_runner.path_helper

    @property
    def messages(self):
        return self.root_runner.messages

    @property
    def env(self):
        return self.root_runner.env

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
