from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class StorageConfig:
    """Storage URI (s3://, file://, etc.)"""

    uri: str
    password: str | None = None
    username: str | None = None


class StoragePort(ABC):
    @abstractmethod
    def save(
        self,
        data: bytes,
        path: str,
    ) -> None:
        pass
