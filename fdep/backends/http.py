from fdep.backends import StorageBackend
import requests


class HTTPBackend(StorageBackend):
    """Implement HTTP/HTTPS."""

    def get_to(self, local_path):
        r = requests.get(self.url, stream=True)
        total_length = int(r.headers.get('content-length', 0))
        self.interpreter.start_progress(total_length)
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
                self.interpreter.progress_callback(len(chunk))
        self.interpreter.end_progress()

    def put_from(self, local_path):
        raise NotImplementedError("HTTP backend does not support uploading")

StorageBackend.register('http', HTTPBackend)
StorageBackend.register('https', HTTPBackend)
