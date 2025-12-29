from dataclasses import dataclass

from fino_core.domain.value.collector import DocumentId, FilingFormat

from .document_metadata import DocumentMetadata


@dataclass
class Document:
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
