from colorama import Fore
from textwrap import dedent

COLOR_TABLE = Fore.__dict__


class FdepDefaultMessages(object):

    USAGE = dedent("""\
    Usage: fdep <command> <arguments>

    fdep installs miscellaneous file dependencies. e.g. datasets, etc.

      help                            Print this helpful message
      version                         Print the currently installed version
      init <envs...>                  Create fdep.yml with specified
                                      environments
      install                         Install dependencies for the project
      upload <local path>             Upload a file to the storage
      add <local path> <remote path>  Add a new dependency to the project
      rm <local path>                 Remove a dependency in the project
    """)

    UNRECOGNIZED_COMMAND =\
        "{RED}Unrecognized command: {{}}{RESET}\n".format(**COLOR_TABLE)

    CURRENT_ENVIRONMENT =\
        "[{CYAN}*{RESET}] Current environment: {{}}".format(**COLOR_TABLE)

    ALREADY_INITIALIZED =\
        "{RED}Already initialized.\n{RESET}".format(**COLOR_TABLE)
    ALREADY_INSTALLED =\
        "[{BLUE}*{RESET}] {{}} is already installed.".format(**COLOR_TABLE)

    INITIALIZED =\
        "Initialized at {}"
    INSTALLING =\
        "[{GREEN}+{RESET}] Installing {BLUE}{{}}{RESET} from {RED}{{}}{RESET}..."\
        .format(**COLOR_TABLE)
    UPLOADING =\
        "[{MAGENTA}#{RESET}] Uploading {BLUE}{{}}{RESET} to {RED}{{}}{RESET}..."\
        .format(**COLOR_TABLE)

    ERROR_NO_FILES_TO_UPLOAD =\
        "{RED}You have to manually specify which files to upload.{RESET}\n"\
        .format(**COLOR_TABLE)
    ERROR_WHILE_UPLOADING =\
        "{RED}Error occurred while uploading{RESET}\n".format(**COLOR_TABLE)
    ERROR_WHILE_INSTALLING =\
        "{RED}Error occurred while installing{RESET}\n".format(**COLOR_TABLE)
    ERROR_MISSING_FDEP =\
        "{RED}Missing fdep.yml. Please run 'fdep init' first!{RESET}\n"\
        .format(**COLOR_TABLE)
    ERROR_NO_SUCH_SECTION_DEFINED =\
        "{RED}No such environment defined in fdep.yml: {{}}{RESET}\n"\
        .format(**COLOR_TABLE)
    ERROR_NO_SUCH_FILE_IN_CONFIG =\
        "{RED}No such file in fdep.yml: {{}}{RESET}\n".format(**COLOR_TABLE)
    ERROR_NO_SUCH_FILE_ON_DISK =\
        "{RED}No such file on the disk: {{}}{RESET}\n".format(**COLOR_TABLE)
    ERROR_UNSUPPORTED_BACKEND =\
        "{RED}Unsupported backend: {{}}{RESET}\n".format(**COLOR_TABLE)
    ERROR_OTHER =\
        "{RED}{{}}{RESET}\n".format(**COLOR_TABLE)
