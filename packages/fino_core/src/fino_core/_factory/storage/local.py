from fino_core._model import StorageInterface


class LocalStorage(StorageInterface):
    def save(self, object: bytes) -> None:
        pass
