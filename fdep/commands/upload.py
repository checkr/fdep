"""Upload a file to the designated storage backend.

.. code:: bash

   fdep upload <files...>

.. note:: Note that just doing ``fdep upload`` doesn't work. You have to specify the file names. We omitted that out in order to emphasize uploading, since it can be destructive.
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


class UploadCommandRunner(SubcommandRunner, ConfigRequiredMixin):
    """Handle upload commands."""
    COMMAND_NAME = 'upload'

    def _task_upload(self, queue, progressbar, vector):
        entry_name, path, source, sha1sum = vector

        progressbar.set_title(entry_name)
        result, _ = StorageBackend.execute(self.root_runner, progressbar, source, 'put_from', path)
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

    def _parallelized_upload(self, to_upload):
        queue = Queue()
        line_filler = lambda: sys.stdout.write('\n' * (len(to_upload) - 1))  # noqa
        line_filler()
        print('\x1b[A' * len(to_upload))
        TqdmProgressBar.set_number_of_progressbars(len(to_upload))
        threads = [
            Thread(
                target=self._task_upload,
                args=(queue, TqdmProgressBar(position=i), v)
            ) for i, v in enumerate(to_upload)
        ]
        for th in threads:
            th.daemon = True
            th.start()

        while queue.qsize() < len(to_upload):
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                line_filler()
                return False

        results = [queue.get() for _ in to_upload]
        line_filler()
        return False not in results

    def run(self, *args, **kwargs):
        if not len(args):
            sys.stderr.write(self.messages.ERROR_NO_FILES_TO_UPLOAD)
            self.root_runner.commands['help'].run()
            return False

        paths = {self.path_helper.resolve_path_to_entry(x) for x in args}
        entries = [(y, self.entries[y]) for y in paths]

        to_upload = []
        for entry_name, entry in entries:
            sha1sum = entry.get('sha1sum')
            version = entry.get('version')
            source = entry.get('source')

            path = self.path_helper.resolve_entry_to_path(entry_name)

            if version:
                source_to_use = '{}_{}'.format(source, version)
            else:
                source_to_use = source

            if os.path.exists(path):
                if sha1sum is not None:
                    new_sha1sum = HashHelper.calculate_sha1sum(path)
                    entry['sha1sum'] = new_sha1sum
            else:
                sys.stderr.write(self.messages.ERROR_NO_SUCH_FILE_ON_DISK.format(entry_name))
                return False

            to_upload.append((entry_name, path, source_to_use, sha1sum))

        if not self._parallelized_upload(to_upload):
            return False

        self.config.save()
        return True
