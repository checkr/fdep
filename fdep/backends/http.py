import requests
from fdep.backends import StorageBackend


class HTTPBackend(StorageBackend):
    """Implement HTTP/HTTPS."""
    SCHEME_NAME = 'http'

    def get_to(self, local_path):
        r = requests.get(self.url, stream=True)
        total_length = int(r.headers.get('content-length', 0))
        self.progressbar.start_progress(total_length)
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(10240):
                f.write(chunk)
                self.progressbar.progress_callback(len(chunk))
        self.progressbar.end_progress()

    def put_from(self, local_path):
        raise NotImplementedError("HTTP backend does not support uploading")


class HTTPSBackend(HTTPBackend):
    SCHEME_NAME = 'https'
