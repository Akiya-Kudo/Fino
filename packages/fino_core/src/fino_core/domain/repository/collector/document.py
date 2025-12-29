from abc import ABC, abstractmethod

from fino_core.domain.entity.collector import Document


class DocumentRepository(ABC):
    @abstractmethod
    def get(self, document_id: str) -> Document: ...

    @abstractmethod
    def store(self, document: Document) -> None: ...
