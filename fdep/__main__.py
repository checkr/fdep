from fdep.config import FdepConfig
from fdep.interpreter import FdepInterpreter
import sys
import os


def main():
    config_path = FdepConfig.find_local_config()
    env = os.environ.get('ENV', 'development')
    interpreter = FdepInterpreter(env, config_path)
    return 0 if interpreter.run(sys.argv[1:]) else 1


if __name__ == '__main__':
    exit(main())
