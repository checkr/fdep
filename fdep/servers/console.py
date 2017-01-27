# -*- coding: utf-8 -*-

import sys

from fdep.servers import RPCServer


class ConsoleServer(RPCServer):
    """Implement a simple console try out interface."""

    def register_functions(self, func_pairs):
        self.funcs = dict(func_pairs)

    def serve_forever(self, **kwargs):
        print("🌝 Try things out!")

        try:
            if not kwargs.get('func'):
                print('We have: {}'.format(', '.join(self.funcs.keys())))
                sys.stdout.write('Which function? ')
                sys.stdout.flush()
                func_name = sys.stdin.readline().strip()
            else:
                func_name = kwargs['func']

            while True:
                sys.stdout.write("? ")
                sys.stdout.flush()
                value = sys.stdin.readline().strip()
                print(self.funcs[func_name](value))
        except KeyboardInterrupt:
            print('')
