from fino_core._model import StorageInterface


class S3Storage(StorageInterface):
    def save(self, object: bytes) -> None:
        pass
