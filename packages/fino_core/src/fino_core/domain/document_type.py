"""Document type definitions for different disclosure sources."""

from dataclasses import dataclass
from enum import Enum, IntEnum, auto


class DisclosureCategory(Enum):
    """業務共通の開示カテゴリ（EDINET/TDNET横断）"""

    FINANCIAL_STATEMENT = auto()
    """財務諸表（有価証券報告書、四半期報告書など）"""
    EVENT = auto()
    """イベント（臨時報告書、適時開示など）"""
    INTERNAL_CONTROL = auto()
    """内部統制"""
    CORPORATE_GOVERNANCE = auto()
    """コーポレートガバナンス"""
    OTHER = auto()
    """その他"""


class EdinetDocumentType(IntEnum):
    """
    EDINET固有の書類種別コード

    value: EDINETコード
    """

    ANNUAL_REPORT = 120
    """有価証券報告書"""
    AMENDED_ANNUAL_REPORT = 130
    """訂正有価証券報告書"""
    QUARTERLY_REPORT = 140
    """四半期報告書"""
    AMENDED_QUARTERLY_REPORT = 150
    """訂正四半期報告書"""
    SEMI_ANNUAL_REPORT = 160
    """半期報告書"""
    AMENDED_SEMI_ANNUAL_REPORT = 170
    """訂正半期報告書"""
    MATERIAL_EVENT_REPORT = 180
    """臨時報告書"""
    PARENT_COMPANY_REPORT = 200
    """親会社等状況報告書"""
    SHARE_REPURCHASE_REPORT = 220
    """自己株券買付状況報告書"""
    AMENDED_SHARE_REPURCHASE_REPORT = 230
    """訂正自己株券買付状況報告書"""
    INTERNAL_CONTROL_REPORT = 235
    """内部統制報告書"""
    AMENDED_INTERNAL_CONTROL_REPORT = 236
    """訂正内部統制報告書"""


class TdnetDocumentType(Enum):
    """
    TDNET固有の書類種別

    value: TDNET識別子
    """

    TIMELY_DISCLOSURE = "timely_disclosure"
    """適時開示"""
    FINANCIAL_STATEMENT = "financial_statement"
    """財務諸表"""
    # TODO: TDNETの実際の書類種別を追加


@dataclass(frozen=True)
class DocumentClassification:
    """
    書類の分類情報

    業務意味の差分を明示的にモデル化する。
    違いを残したまま共通化する。
    """

    source: "DisclosureSource"
    """開示元（EDINET/TDNET）"""
    category: DisclosureCategory
    """業務共通カテゴリ"""
    raw_type: str | int
    """開示元固有の書類種別（EDINETコード、TDNET識別子など）"""

    @classmethod
    def from_edinet(cls, doc_type: EdinetDocumentType) -> "DocumentClassification":
        """EDINET書類種別から分類を作成"""
        from .document import DisclosureSource

        # EDINET書類種別を業務カテゴリにマッピング
        category_map = {
            EdinetDocumentType.ANNUAL_REPORT: DisclosureCategory.FINANCIAL_STATEMENT,
            EdinetDocumentType.AMENDED_ANNUAL_REPORT: DisclosureCategory.FINANCIAL_STATEMENT,
            EdinetDocumentType.QUARTERLY_REPORT: DisclosureCategory.FINANCIAL_STATEMENT,
            EdinetDocumentType.AMENDED_QUARTERLY_REPORT: DisclosureCategory.FINANCIAL_STATEMENT,
            EdinetDocumentType.SEMI_ANNUAL_REPORT: DisclosureCategory.FINANCIAL_STATEMENT,
            EdinetDocumentType.AMENDED_SEMI_ANNUAL_REPORT: DisclosureCategory.FINANCIAL_STATEMENT,
            EdinetDocumentType.MATERIAL_EVENT_REPORT: DisclosureCategory.EVENT,
            EdinetDocumentType.PARENT_COMPANY_REPORT: DisclosureCategory.CORPORATE_GOVERNANCE,
            EdinetDocumentType.SHARE_REPURCHASE_REPORT: DisclosureCategory.CORPORATE_GOVERNANCE,
            EdinetDocumentType.AMENDED_SHARE_REPURCHASE_REPORT: DisclosureCategory.CORPORATE_GOVERNANCE,
            EdinetDocumentType.INTERNAL_CONTROL_REPORT: DisclosureCategory.INTERNAL_CONTROL,
            EdinetDocumentType.AMENDED_INTERNAL_CONTROL_REPORT: DisclosureCategory.INTERNAL_CONTROL,
        }

        return cls(
            source=DisclosureSource.EDINET,
            category=category_map.get(doc_type, DisclosureCategory.OTHER),
            raw_type=doc_type.value,
        )

    @classmethod
    def from_tdnet(cls, doc_type: TdnetDocumentType) -> "DocumentClassification":
        """TDNET書類種別から分類を作成"""
        from .document import DisclosureSource

        # TDNET書類種別を業務カテゴリにマッピング
        category_map = {
            TdnetDocumentType.TIMELY_DISCLOSURE: DisclosureCategory.EVENT,
            TdnetDocumentType.FINANCIAL_STATEMENT: DisclosureCategory.FINANCIAL_STATEMENT,
        }

        return cls(
            source=DisclosureSource.TDNET,
            category=category_map.get(doc_type, DisclosureCategory.OTHER),
            raw_type=doc_type.value,
        )
