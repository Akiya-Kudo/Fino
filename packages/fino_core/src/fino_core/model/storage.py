"""Storage configuration and port definitions."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class StorageConfig(ABC):
    """基底クラス: ストレージ設定の共通インターフェース"""

    pass


@dataclass
class LocalStorageConfig(StorageConfig):
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
        """
        データを保存する

        Args:
            key: 保存先のキー（パス）
            data: 保存するデータ
        """
        pass

    @abstractmethod
    def get(self, key: str) -> bytes:
        """
        データを取得する

        Args:
            key: 取得するキー（パス）

        Returns:
            取得したデータ
        """
        pass
