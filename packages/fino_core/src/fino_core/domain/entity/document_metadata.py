from dataclasses import dataclass

from ..value import (
    DisclosureType,
    DocumentId,
    FilingDate,
    FilingFormat,
    FilingLanguage,
    Source,
    Ticker,
)


@dataclass
class DocumentMetadata:
    """文書のメタデータを表現するドメインエンティティ"""

    document_id: DocumentId
    source: Source
    title: str
    ticker: Ticker
    filing_language: FilingLanguage
    filing_format: FilingFormat
    filing_date: FilingDate
    disclosure_type: DisclosureType

    def __post_init__(self) -> None:
        """ドメイン不変条件の検証"""
        if not self.title or not self.title.strip():
            raise ValueError("title must not be empty")
