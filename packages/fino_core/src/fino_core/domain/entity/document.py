from dataclasses import dataclass

from fino_core.domain.entity.entity import AggregateRoot
from fino_core.domain.value import DocumentId, FilingFormat

from .document_metadata import DocumentMetadata


# @see: about dataclass annotation:  https://qiita.com/fumiya0238/items/46115b399c4ea1322ee8
@dataclass(kw_only=True, slots=True, eq=False)
class Document(AggregateRoot):
    """文書本体を表現するドメインエンティティ

    DocumentはDocumentMetadataを含み、実際の文書データ（resource）を保持します。
    """

    document_id: DocumentId
    metadata: DocumentMetadata
    name: str
    filing_format: FilingFormat
    resource: bytes | None = None

    def __post_init__(self) -> None:
        """ドメイン不変条件の検証"""
        if not self.name or not self.name.strip():
            raise ValueError("name must not be empty")
        if self.resource is not None and len(self.resource) == 0:
            raise ValueError("resource must not be empty bytes if provided")
