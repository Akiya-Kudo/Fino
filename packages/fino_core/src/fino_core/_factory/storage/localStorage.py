from fino_core.model import StorageInterface


class LocalStorage(StorageInterface):
    def save(self, object: bytes) -> None:
        pass
