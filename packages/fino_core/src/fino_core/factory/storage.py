from typing import TYPE_CHECKING

from fino_core.infrastructure.storage.local_storage import LocalStorage
from fino_core.infrastructure.storage.s3_storage import S3Storage
from fino_core.model.storage import (
    LocalStorageConfig,
    S3StorageConfig,
    Storage,
    StorageConfig,
)

if TYPE_CHECKING:
    pass


def create_storage(config: StorageConfig) -> Storage:
    if isinstance(config, LocalStorageConfig):
        return LocalStorage(config.base_path)

    if isinstance(config, S3StorageConfig):
        return S3Storage(
            bucket=config.bucket,
            api_key=config.api_key,
            region=config.region,
        )

    raise ValueError(f"Unknown StorageConfig type: {type(config)}")
