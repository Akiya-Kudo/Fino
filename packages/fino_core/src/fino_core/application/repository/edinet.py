from abc import ABC, abstractmethod
from datetime import date

from fino_core.domain.model.document.document_metadata import DocumentMetadata


class EdinetRepository(ABC):
    @abstractmethod
    def get_document_list(self, date: date, withdocs: bool = False) -> DocumentMetadata: ...
    @abstractmethod
    def get_document(self, doc_id: str, doc_type: EdinetDocType) -> bytes: ...
