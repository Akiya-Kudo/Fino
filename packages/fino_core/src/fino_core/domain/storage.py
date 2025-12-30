"""Storage configuration and port definitions."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class StorageConfig(ABC):  # noqa: B024
    """基底クラス: ストレージ設定の共通インターフェース"""


@dataclass
class LocalStorageConfig(StorageConfig):  # noqa: B024
    """ローカルストレージの設定"""

    base_path: str


@dataclass
class S3StorageConfig(StorageConfig):
    """S3ストレージの設定"""

    bucket: str
    api_key: str
    region: str


class StoragePort(ABC):
    """ストレージ操作のポート（インターフェース）"""

    @abstractmethod
    def save(self, key: str, data: bytes) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> bytes:
        pass


# 型エイリアス（後方互換性のため）
Storage = StoragePort
