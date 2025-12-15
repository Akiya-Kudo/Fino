from urllib.parse import urlparse

from fino_core._model.storage import StorageConfig, StorageInterface

from .local_storage import LocalStorage
from .s3_storage import S3Storage


def create_storage(config: StorageConfig) -> StorageInterface:
    parsed = urlparse(config.storage_path)
    if parsed.scheme == "s3" or parsed.hostname == "localhost" or parsed.hostname == "127.0.0.1":
        return S3Storage(config.storage_path)
    elif parsed.scheme == "":
        return LocalStorage(config.storage_path)
    else:
        raise ValueError(f"Factory Error: create_storage: Unsupported storage scheme: {parsed}")
