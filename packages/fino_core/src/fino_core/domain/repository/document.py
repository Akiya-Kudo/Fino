from abc import ABC, abstractmethod

from ..entity.document import Document


class DocumentRepository(ABC):
    @abstractmethod
    def get(self, document_id: str) -> Document: ...

    @abstractmethod
    def store(self, document: Document) -> None: ...
