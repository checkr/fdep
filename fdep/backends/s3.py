import os

import boto3
from fdep.backends import StorageBackend
from fdep.utils import urlparse
from threading import Lock


class S3Backend(StorageBackend):
    """Implement AWS S3."""
    SCHEME_NAME = 's3'
    BOTO_SESSION_LOCK = Lock()

    def _get_object(self, client, bucket, key):
        return client.get_object(Bucket=bucket, Key=key)

    def _prepare_s3(self, local_path=None):
        o = urlparse(self.url)
        bucket = o.netloc
        key = o.path[1:]

        # Boto3 is not thread-safe
        self.__class__.BOTO_SESSION_LOCK.acquire(True)
        client = boto3.client('s3')
        self.__class__.BOTO_SESSION_LOCK.release()

        if local_path is not None:
            total_length = os.stat(local_path).st_size
        else:
            total_length = self._get_object(
                client, bucket, key).get('ContentLength', 0)
        self.progressbar.start_progress(total_length)
        return client, bucket, key

    def get_to(self, local_path):
        client, bucket, key = self._prepare_s3()
        client.download_file(
            bucket, key, local_path,
            Callback=self.progressbar.progress_callback
        )
        self.progressbar.end_progress()

    def put_from(self, local_path):
        client, bucket, key = self._prepare_s3(local_path)
        client.upload_file(
            local_path, bucket, key,
            Callback=self.progressbar.progress_callback
        )
        self.progressbar.end_progress()
