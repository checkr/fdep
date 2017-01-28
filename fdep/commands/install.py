"""Install dependencies for the project.

.. code:: bash

   fdep install [<files...>]
"""
import os
import sys
import time
from threading import Thread

from fdep.backends import StorageBackend
from fdep.commands import ConfigRequiredMixin, SubcommandRunner
from fdep.interfaces.progressbar import TqdmProgressBar
from fdep.utils import HashHelper

try:
    from Queue import Queue
except ImportError:
    from queue import Queue


class InstallCommandRunner(SubcommandRunner, ConfigRequiredMixin):
    """Handle install commands."""
    COMMAND_NAME = 'install'

    def _task_install(self, queue, progressbar, vector):
        entry_name, path, source, sha1sum = vector

        progressbar.set_title(entry_name)
        result, _ = StorageBackend.execute(self.root_runner, progressbar, source, 'get_to', path)
        if not result:
            sys.stderr.write(self.messages.ERROR_WHILE_INSTALLING)
            queue.put(False)
            return

        if sha1sum is not None:
            new_sha1sum = HashHelper.calculate_sha1sum(path)
            if sha1sum != new_sha1sum:
                sys.stderr.write(self.messages.ERROR_WRONG_SHA1SUM.format(sha1sum, new_sha1sum))
                os.unlink(path)  # Clean up the wrong one.
                queue.put(False)
                return
        queue.put(True)

    def _parallelized_install(self, to_install):
        queue = Queue()
        line_filler = lambda: sys.stdout.write('\n' * (len(to_install) - 1))  # noqa
        line_filler()
        print('\x1b[A' * len(to_install))
        TqdmProgressBar.set_number_of_progressbars(len(to_install))
        threads = [
            Thread(
                target=self._task_install,
                args=(queue, TqdmProgressBar(position=i), v)
            ) for i, v in enumerate(to_install)
        ]
        for th in threads:
            th.daemon = True
            th.start()

        while queue.qsize() < len(to_install):
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                line_filler()
                return False

        results = [queue.get() for _ in to_install]
        line_filler()
        return False not in results

    def run(self, *args, **kwargs):
        if not len(args):
            entries = self.entries.items()
        else:
            paths = {self.path_helper.resolve_path_to_entry(x) for x in args}
            entries = [(y, self.entries[y]) for y in paths]

        to_install = []
        for entry_name, entry in entries:
            sha1sum = entry.get('sha1sum')
            version = entry.get('version')
            source = entry.get('source')

            path = self.path_helper.resolve_entry_to_path(entry_name)
            self.path_helper.ensure_directories(os.path.dirname(path))

            if version:
                source_to_use = '{}_{}'.format(source, version)
            else:
                source_to_use = source

            if os.path.exists(path):
                if sha1sum is not None:
                    actual_sha1sum = HashHelper.calculate_sha1sum(path)
                    if sha1sum != actual_sha1sum:
                        print(self.messages.FILE_CHANGED.format(entry_name))
                        return False
                print(self.messages.ALREADY_INSTALLED.format(entry_name))
                continue

            to_install.append((entry_name, path, source_to_use, sha1sum))

        if not self._parallelized_install(to_install):
            return False
        return True
