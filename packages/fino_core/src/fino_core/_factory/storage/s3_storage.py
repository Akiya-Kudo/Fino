from fino_core._model.storage import Storage, StoragePort


class S3Storage(StoragePort):
    def __init__(self, config: Storage) -> None:
        self.config = config

    def save(self, object: bytes) -> None:
        pass

    def hoge(self, object: bytes) -> None:
        pass
