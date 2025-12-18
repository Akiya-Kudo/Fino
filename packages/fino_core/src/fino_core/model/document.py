"""Document domain entity."""

from dataclasses import dataclass
from enum import Enum

from .document_type import DocumentClassification


class DisclosureSource(Enum):
    """
    開示元（Disclosure Source）

    業務的にクリティカルな差分をDomain層で明示的にモデル化する。
    「どこ由来か」は業務意味を持つ。
    """

    EDINET = "edinet"
    """EDINET（金融庁）"""
    TDNET = "tdnet"
    """TDNET（適時開示情報）"""


@dataclass(frozen=True)
class Document:
    """
    書類エンティティ

    業務的にクリティカルな差分をDomain層で明示的にモデル化する。
    """

    id: str
    """書類ID（docIDなど）"""
    source: DisclosureSource
    """開示元（業務意味を持つ）"""
    classification: DocumentClassification
    """書類分類（業務意味の差分を表現）"""
    ticker: str | None = None
    """証券コード"""
    format_type: str | None = None
    """フォーマット種別（XBRL、PDFなど）"""
