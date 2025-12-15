from abc import ABCMeta, abstractmethod
from typing import Optional

from pydantic import BaseModel


class StorageConfig(BaseModel):
    storage_path: str
    password: Optional[str] = None
    username: Optional[str] = None


class StorageRepository(ABCMeta):
    @abstractmethod
    def save(
        cls, object: bytes
    ) -> None: ...  # @see: https://stackoverflow.com/questions/73792674/python-protocol-use-static-method-or-ellipsis
