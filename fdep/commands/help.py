from fdep.commands import SubcommandRunner


class HelpCommandRunner(SubcommandRunner):
    """Handle help commands."""
    COMMAND_NAME = 'help'

    def run(self, *args, **kwargs):
        print(self.messages.USAGE)
