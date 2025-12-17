from fino_core._model.storage import Storage, StoragePort


class LocalStorage(StoragePort):
    def __init__(self, config: Storage) -> None:
        self.config = config

    def save(self, object: bytes) -> None:
        pass
