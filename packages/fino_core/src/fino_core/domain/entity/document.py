from dataclasses import dataclass

from ..value import FilingFormat
from .document_metadata import DocumentMetadata


@dataclass
class Document:
    """文書本体を表現するドメインエンティティ

    DocumentはDocumentMetadataを含み、実際の文書データ（resource）を保持します。
    """

    metadata: DocumentMetadata
    name: str
    resource: bytes | None = None

    def __post_init__(self) -> None:
        """ドメイン不変条件の検証"""
        if not self.name or not self.name.strip():
            raise ValueError("name must not be empty")
        if self.resource is not None and len(self.resource) == 0:
            raise ValueError("resource must not be empty bytes if provided")

    @property
    def document_id(self) -> str:
        """document_idへのショートカット（後方互換性のため）"""
        return str(self.metadata.document_id)

    @property
    def filing_format(self) -> FilingFormat:
        """filing_formatへのショートカット（後方互換性のため）"""
        return self.metadata.filing_format
