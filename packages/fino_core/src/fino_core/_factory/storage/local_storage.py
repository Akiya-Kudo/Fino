from fino_core._model.storage import StorageRepository


class LocalStorage(StorageRepository):
    def save(self, object: bytes) -> None:
        pass
