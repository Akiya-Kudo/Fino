from urllib.parse import urlparse

from fino_core._factory.storage.local import LocalStorage
from fino_core._factory.storage.s3 import S3Storage
from fino_core._model import Storage, StorageInterface


def create_storage(storage: Storage) -> StorageInterface:
    parsed = urlparse(storage.storage_uri)
    if (
        parsed.scheme == "s3"
        or parsed.hostname == "localhost"
        or parsed.hostname == "127.0.0.1"
    ):
        return S3Storage(storage.storage_uri)
    elif parsed.scheme == "":
        return LocalStorage(storage.storage_uri)
    else:
        raise ValueError(
            f"Factory Error: create_storage: Unsupported storage scheme: {parsed}"
        )
