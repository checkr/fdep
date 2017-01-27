import sys
import time
from abc import ABCMeta, abstractmethod
from threading import Lock

from tqdm import tqdm


class ProgressBar(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start_progress(self, length):
        pass

    @abstractmethod
    def progress_callback(self, length):
        pass

    @abstractmethod
    def end_progress(self):
        pass


class TqdmProgressBar(ProgressBar):
    """Implement a thread-safe tqdm progressbar.

    This can be used in multiple threads.
    """
    PROGRESSBAR_UPDATE_LOCK = Lock()
    N_PROGRESSBARS = 1
    CREATED_PROGRESSBARS = []
    STARTED_PROGRESSBARS = []
    FINISHED_PROGRESSBARS = []

    @classmethod
    def lock(cls):
        cls.PROGRESSBAR_UPDATE_LOCK.acquire(True)

    @classmethod
    def unlock(cls):
        cls.PROGRESSBAR_UPDATE_LOCK.release()

    @classmethod
    def set_number_of_progressbars(cls, n):
        cls.N_PROGRESSBARS = n

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.position = kwargs.get('position')
        self.tqdm = None
        TqdmProgressBar.lock()
        TqdmProgressBar.CREATED_PROGRESSBARS.append(self)
        TqdmProgressBar.unlock()

    def set_title(self, title):
        self.title = title
        if self.tqdm:
            self.tqdm.set_description(title)

    def start_progress(self, length):
        """Set up the progress bar.

        This is a callback function from the storage backend.
        """
        if sys.version_info.major <= 2:
            use_ascii = True
        else:
            use_ascii = False

        kwargs = {
            'total': length,
            'unit': 'B',
            'unit_scale': True,
            'ascii': use_ascii,
            'leave': True,
            'dynamic_ncols': True,
            'miniters': 1,
        }

        if self.position is not None:
            kwargs['position'] = self.position

        if self.title is not None:
            kwargs['desc'] = self.title

        self.tqdm = tqdm(**kwargs)
        TqdmProgressBar.lock()
        TqdmProgressBar.STARTED_PROGRESSBARS.append(self)
        TqdmProgressBar.unlock()

    def progress_callback(self, length):
        """Update the progress bar's progress.

        This is a callback function from the storage backend.
        """
        TqdmProgressBar.lock()
        self.tqdm.update(length)
        TqdmProgressBar.unlock()

    def end_progress(self):
        """Clean up the progress bar.

        This is a callback function from the storage backend.
        """
        TqdmProgressBar.lock()
        if len(TqdmProgressBar.CREATED_PROGRESSBARS) == TqdmProgressBar.N_PROGRESSBARS and\
                len(TqdmProgressBar.FINISHED_PROGRESSBARS) == (TqdmProgressBar.N_PROGRESSBARS - 1) and\
                len(TqdmProgressBar.STARTED_PROGRESSBARS) == 1:
            for progressbar in TqdmProgressBar.CREATED_PROGRESSBARS:
                progressbar.tqdm.close()
            TqdmProgressBar.CREATED_PROGRESSBARS = []
            TqdmProgressBar.STARTED_PROGRESSBARS = []
            TqdmProgressBar.FINISHED_PROGRESSBARS = []
            TqdmProgressBar.N_PROGRESSBARS = 1
        else:
            self.tqdm.last_print_n = self.tqdm.last_print_t = 0
            self.tqdm.update(max(0, self.tqdm.total - self.tqdm.n))
            TqdmProgressBar.STARTED_PROGRESSBARS.remove(self)
            TqdmProgressBar.FINISHED_PROGRESSBARS.append(self)
        TqdmProgressBar.unlock()
