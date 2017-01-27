from fdep.backends import StorageBackend
from fdep.backends.http import HTTPSBackend


class GSpreadsheetBackend(HTTPSBackend):
    """Implement Google Spreadsheet.

    This backend only supports downloading gdocs shared with anyone who has the link.
    """
    SCHEME_NAME = 'gspreadsheet'

    def __init__(self, *args, **kwargs):
        HTTPSBackend.__init__(self, *args, **kwargs)
        self.key = self.url.split('/')[-1]
        self.url = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv'.format(self.key)

    def put_from(self, local_path):
        raise NotImplementedError("Google Spreadsheet backend does not support uploading")
