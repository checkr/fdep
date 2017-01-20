from fdep.backends.http import HTTPBackend
from fdep.backends import StorageBackend


class GSpreadsheetBackend(HTTPBackend):
    """Implement Google Spreadsheet.

    This backend only supports downloading gdocs shared with anyone who has the link.
    """

    def __init__(self, *args, **kwargs):
        HTTPBackend.__init__(self, *args, **kwargs)
        self.key = self.url.split('/')[-1]
        self.url = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(self.key)

    def put_from(self, local_path):
        raise NotImplementedError("Google Spreadsheet backend does not support uploading")

StorageBackend.register('gspreadsheet', GSpreadsheetBackend)
