from fino_core.model.period import Period

from .input.collect_document import CollectDocumentInput


def collect_documents(input: CollectDocumentInput) -> None:
    period = Period.from_input(input.period)
    # TODO: StorageInputからStorageConfigへの変換を実装
    # storage = create_storage(input.storage)
