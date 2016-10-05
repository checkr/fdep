from fdep.backends import StorageBackend
from fdep.utils import urlparse
import boto3
import os


class S3Backend(StorageBackend):
    """Implement AWS S3."""

    def _get_object(self, client, bucket, key):
        return client.get_object(Bucket=bucket, Key=key)

    def _prepare_s3(self, local_path=None):
        o = urlparse(self.url)
        bucket = o.netloc
        key = o.path[1:]
        client = boto3.client('s3')
        if local_path is not None:
            total_length = os.stat(local_path).st_size
        else:
            total_length = self._get_object(
                client, bucket, key).get('ContentLength', 0)
        self.interpreter.start_progress(total_length)
        return client, bucket, key

    def get_to(self, local_path):
        client, bucket, key = self._prepare_s3()
        client.download_file(
            bucket, key, local_path,
            Callback=self.interpreter.progress_callback
        )
        self.interpreter.end_progress()

    def put_from(self, local_path):
        client, bucket, key = self._prepare_s3(local_path)
        client.upload_file(
            local_path, bucket, key,
            Callback=self.interpreter.progress_callback
        )
        self.interpreter.end_progress()

StorageBackend.register('s3', S3Backend)
