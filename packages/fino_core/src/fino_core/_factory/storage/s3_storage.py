from fino_core._model.storage import StorageRepository


class S3Storage(StorageRepository):
    def save(self, object: bytes) -> None:
        pass

    def hoge(self, object: bytes) -> None:
        pass
