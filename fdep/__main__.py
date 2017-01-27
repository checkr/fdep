import os
import sys

from fdep.config import FdepConfig
from fdep.runner import FdepRunner


def parse_argv(argv):
    """Implement a manual option parser."""
    argv = list(argv)
    args, kwargs = [], {}

    while len(argv):
        arg = argv.pop(0)
        if arg[0] == '-' and len(arg) >= 2:
            ind = 2 if arg[1] == '-' else 1
            kv = arg[ind:].split('=', 1)
            if len(kv) == 1:
                kv.append(argv.pop(0))
            kwargs[kv[0]] = kv[1]
        else:
            args.append(arg)
    return args, kwargs


def main(argv=None):
    """Implement the entry point of fdep."""
    if argv is None:
        argv = sys.argv
    root_path = FdepConfig.find_root_path() or os.getcwd()
    env = os.environ.get('ENV', 'development')
    config = FdepConfig.load(os.path.join(root_path, 'fdep.yml'))
    runner = FdepRunner(env, config)
    args, kwargs = parse_argv(argv[1:])
    if not runner.run(*args, **kwargs):
        return 1
    return 0


if __name__ == '__main__':
    exit(main(sys.argv))
