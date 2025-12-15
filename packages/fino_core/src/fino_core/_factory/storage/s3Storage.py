from fino_core.model import StorageInterface


class S3Storage(StorageInterface):
    def save(self, object: bytes) -> None:
        pass

    def hoge(self, object: bytes) -> None:
        pass
