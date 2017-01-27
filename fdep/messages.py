from textwrap import dedent

from colorama import Fore

COLOR_TABLE = Fore.__dict__


class FdepDefaultMessages(object):

    USAGE = dedent("""\
    Usage: {LIGHTWHITE_EX}fdep{RESET} {GREEN}<command>{RESET} <arguments>

    fdep delivers models, datasets from development to production.

      {GREEN}help{RESET}                            Print this helpful message
      {GREEN}version{RESET}                         Print the currently installed version
      {GREEN}init{RESET} <envs...>                  Create fdep.yml with specified
                                      environments
      {GREEN}install{RESET}                         Install dependencies for the project
      {GREEN}upload{RESET} <local path>             Upload a file to the storage
      {GREEN}commit{RESET} <local path>             Upload a file to the storage with a versioning tag
      {GREEN}add{RESET} <local path> <remote path> [<version>]
                                      Add a new dependency to the project
      {GREEN}rm{RESET} <local path>                 Remove a dependency in the project
    """.format(**COLOR_TABLE))

    UNRECOGNIZED_COMMAND =\
        "{RED}Unrecognized command: {{}}{RESET}\n".format(**COLOR_TABLE)

    FDEP_LOCAL_VERSION = " Local version: {GREEN}{{}}{RESET}".format(**COLOR_TABLE)
    FDEP_RECENT_VERSION = "Recent version: {GREEN}{{}}{RESET}".format(**COLOR_TABLE)
    FDEP_NEW_VERSION_EXISTS = ("{RED}There is a new version." +\
        "Please upgrade fdep by the following command:\n\tpip install -U fdep{RESET}").format(**COLOR_TABLE)

    CURRENT_ENVIRONMENT =\
        "[{CYAN}*{RESET}] Current environment: {YELLOW}{{}}{RESET}".format(**COLOR_TABLE)

    ALREADY_INITIALIZED =\
        "{RED}Already initialized.\n{RESET}".format(**COLOR_TABLE)
    ALREADY_INSTALLED =\
        "[{BLUE}*{RESET}] {BLUE}{{}}{RESET} is already installed.".format(**COLOR_TABLE)
    FILE_CHANGED =\
        ("[{BLUE}*{RESET}] {BLUE}{{}}{RESET} is already installed. But, it looks like it was changed " +\
        "since it was downloaded. Upload your file, or delete the file and " +\
        "re-install it.").format(**COLOR_TABLE)

    NEW_VERSION_UPLOADED =\
        ("New version {{}} of {BLUE}{{}}{RESET} has been uploaded. Make sure you commit the changed fdep.yml " +\
        "on your version control software as well.").format(**COLOR_TABLE)

    FROZEN =\
        "{GREEN}{{}}{RESET} has been frozen.".format(**COLOR_TABLE)
    UNFROZEN =\
        "{GREEN}{{}}{RESET} has been unfrozen.".format(**COLOR_TABLE)
    ADDED =\
        "{GREEN}{{}}{RESET} has been added to the list.".format(**COLOR_TABLE)
    REMOVED =\
        "{GREEN}{{}}{RESET} has been removed from the list.".format(**COLOR_TABLE)
    RENAMED =\
        "{GREEN}{{}}{RESET} has been renamed as {GREEN}{{}}{RESET}.".format(**COLOR_TABLE)
    LINKED =\
        "{GREEN}{{}}{RESET} has been linked with {GREEN}{{}}{RESET}.".format(**COLOR_TABLE)
    INITIALIZED =\
        "Initialized empty fdep configuration in {GREEN}{{}}/fdep.yml{RESET}".format(**COLOR_TABLE)

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
    ERROR_WRONG_SHA1SUM =\
        "{RED}Wrong SHA1SUM: {{}} != {{}}{RESET}\n".format(**COLOR_TABLE)
    ERROR_INVALID_ARGUMENT =\
        "{RED}Wrong number of arguments or invalid arguments.{RESET}\n".format(**COLOR_TABLE)
    ERROR_OTHER =\
        "{RED}{{}}{RESET}\n".format(**COLOR_TABLE)
