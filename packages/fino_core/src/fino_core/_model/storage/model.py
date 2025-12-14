from typing import Optional, Protocol

from pydantic import BaseModel


class Storage(BaseModel):
    storage_path: str
    password: Optional[str] = None
    username: Optional[str] = None


class StorageInterface(Protocol):
    def save(
        self, object: bytes
    ) -> None: ...  # @see: https://stackoverflow.com/questions/73792674/python-protocol-use-static-method-or-ellipsis
