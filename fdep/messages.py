# -*- coding: utf-8 -*-
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

    FDEP_LOCAL_VERSION = " Local version: {GREEN}{{}}{RESET}".format(**COLOR_TABLE)
    FDEP_RECENT_VERSION = "Recent version: {GREEN}{{}}{RESET}".format(**COLOR_TABLE)
    FDEP_NEW_VERSION_EXISTS = ("{RED}There is a new version." +\
        "Please upgrade fdep by the following command:\n\tpip install -U fdep{RESET}").format(**COLOR_TABLE)

    CURRENT_ENVIRONMENT =\
        "{CYAN}⚓{RESET} Current environment: {YELLOW}{{}}{RESET}".format(**COLOR_TABLE)

    ALREADY_INSTALLED =\
        "· {BLUE}{{}}{RESET} is already installed.".format(**COLOR_TABLE)
    FILE_CHANGED =\
        ("· {BLUE}{{}}{RESET} is already installed. But, it looks like it was changed " +\
        "since it was downloaded. Upload your file, or delete the file and " +\
        "re-install it.").format(**COLOR_TABLE)

    NEW_VERSION_UPLOADED =\
        ("New version {{}} of {BLUE}{{}}{RESET} has been uploaded. Make sure you commit the changed fdep.yml " +\
        "on your version control software as well.").format(**COLOR_TABLE)

    FROZEN =\
        "{GREEN}✓{RESET} {BLUE}{{}}{RESET} has been frozen.".format(**COLOR_TABLE)
    UNFROZEN =\
        "{GREEN}✓{RESET} {BLUE}{{}}{RESET} has been unfrozen.".format(**COLOR_TABLE)
    ADDED =\
        "{GREEN}✓{RESET} {BLUE}{{}}{RESET} has been added to the list.".format(**COLOR_TABLE)
    REMOVED =\
        "{GREEN}✓{RESET} {BLUE}{{}}{RESET} has been removed from the list.".format(**COLOR_TABLE)
    RENAMED =\
        "{GREEN}✓{RESET} {BLUE}{{}}{RESET} has been renamed as {BLUE}{{}}{RESET}.".format(**COLOR_TABLE)
    LINKED =\
        "{GREEN}✓{RESET} {BLUE}{{}}{RESET} has been linked with {BLUE}{{}}{RESET}.".format(**COLOR_TABLE)
    INITIALIZED =\
        "{GREEN}✓{RESET} Initialized empty fdep configuration in {BLUE}{{}}/fdep.yml{RESET}".format(**COLOR_TABLE)
    SERVING =\
        "🌎  {BLUE}{{}} for {{}}{RESET} is running at :{{}}".format(**COLOR_TABLE)

    UNRECOGNIZED_COMMAND =\
        "{RED}✘{RESET} Unrecognized command: {{}}\n".format(**COLOR_TABLE)

    ALREADY_INITIALIZED =\
        "{RED}✘{RESET} Already initialized.\n".format(**COLOR_TABLE)

    ERROR_NO_SUCH_MODULE =\
        "{RED}✘{RESET} Module {{}} cannot be loaded.\n".format(**COLOR_TABLE)
    ERROR_NO_FILES_TO_UPLOAD =\
        "{RED}✘{RESET} You have to manually specify which files to upload.\n"\
        .format(**COLOR_TABLE)
    ERROR_WHILE_UPLOADING =\
        "{RED}✘{RESET} Error occurred while uploading\n".format(**COLOR_TABLE)
    ERROR_WHILE_INSTALLING =\
        "{RED}✘{RESET} Error occurred while installing\n".format(**COLOR_TABLE)
    ERROR_MISSING_FDEP =\
        "{RED}✘{RESET} Missing fdep.yml. Please run 'fdep init' first!\n"\
        .format(**COLOR_TABLE)
    ERROR_NO_SUCH_SECTION_DEFINED =\
        "{RED}✘{RESET} No such environment defined in fdep.yml: {{}}\n"\
        .format(**COLOR_TABLE)
    ERROR_NO_SUCH_FILE_IN_CONFIG =\
        "{RED}✘{RESET} No such file in fdep.yml: {{}}\n".format(**COLOR_TABLE)
    ERROR_NO_SUCH_FILE_ON_DISK =\
        "{RED}✘{RESET} No such file on the disk: {{}}\n".format(**COLOR_TABLE)
    ERROR_UNSUPPORTED_BACKEND =\
        "{RED}✘{RESET} Unsupported backend: {{}}\n".format(**COLOR_TABLE)
    ERROR_WRONG_SHA1SUM =\
        "{RED}✘{RESET} Wrong SHA1SUM: {{}} != {{}}\n".format(**COLOR_TABLE)
    ERROR_INVALID_ARGUMENT =\
        "{RED}✘{RESET} Wrong number of arguments or invalid arguments.\n".format(**COLOR_TABLE)
    ERROR_OTHER =\
        "{RED}✘{RESET} {{}}\n".format(**COLOR_TABLE)
