"""Storage factory for creating storage instances."""

# 循環インポートを避けるため、実装クラスは関数内でインポート
from typing import TYPE_CHECKING

from fino_core.model.storage import (
    LocalStorageConfig,
    S3StorageConfig,
    StorageConfig,
    StoragePort,
)

if TYPE_CHECKING:
    pass


def create_storage(config: StorageConfig) -> StoragePort:
    """
    ストレージ設定からストレージインスタンスを生成するFactory関数

    Args:
        config: ストレージ設定（LocalStorageConfig または S3StorageConfig）

    Returns:
        ストレージポートの実装インスタンス

    Raises:
        ValueError: 未知のStorageConfig型が渡された場合
    """
    if isinstance(config, LocalStorageConfig):
        from fino_core.infrastructure.storage.local_storage import LocalStorage

        return LocalStorage(config.base_path)

    if isinstance(config, S3StorageConfig):
        from fino_core.infrastructure.storage.s3_storage import S3Storage

        return S3Storage(
            bucket=config.bucket,
            api_key=config.api_key,
            region=config.region,
        )

    raise ValueError(f"Unknown StorageConfig type: {type(config)}")
