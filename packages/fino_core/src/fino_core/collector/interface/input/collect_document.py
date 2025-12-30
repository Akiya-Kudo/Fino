from typing import TypedDict
from fino_core.util import TimeScope


class CollectEdinetDocumentInput(TypedDict):
    storage_config: StorageConfig
    api_key: str
    timescope: TimeScope
    doc_types = ([EdinetDocType.ANNUAL_REPORT],)
