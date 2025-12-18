from fino_core.api.collector.input.collect_document import CollectDocumentInput
from fino_core.model.period import Period


def collect_documents(input: CollectDocumentInput) -> None:
    period = Period.from_input(input.period)
    # TODO: StorageInputからStorageConfigへの変換を実装
    # storage = create_storage(input.storage)
