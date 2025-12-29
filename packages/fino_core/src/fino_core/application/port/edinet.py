from abc import ABC, abstractmethod
from datetime import date

from fino_core.domain.entity.document import Document
from fino_core.domain.entity.document_metadata import DocumentMetadata
from fino_core.domain.value import DisclosureType


class EdinetRepository(ABC):
    @abstractmethod
    def get_document_list(self, date: date, withdocs: bool = False) -> list[DocumentMetadata]: ...
    @abstractmethod
    def get_document(self, doc_id: str, doc_type: DisclosureType) -> Document: ...
