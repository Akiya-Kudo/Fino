from enum import Enum, auto
from typing import Union

from .edinet.main import EdinetTargetConfig, EdinetTargetPort


class TargetType(Enum):
    EDINET = auto()


class FormatType(Enum):
    XBRL = auto()
    PDF = auto()
    CSV = auto()


class DocType(Enum):
    ANNUAL_REPORT = auto()
    """有価証券報告書"""
    AMENDED_ANNUAL_REPORT = auto()
    """訂正有価証券報告書"""
    QUARTERLY_REPORT = auto()
    """四半期報告書"""
    AMENDED_QUARTERLY_REPORT = auto()
    """訂正四半期報告書"""
    SEMI_ANNUAL_REPORT = auto()
    """半期報告書"""
    AMENDED_SEMI_ANNUAL_REPORT = auto()
    """訂正半期報告書"""
    INTERNAL_CONTROL_REPORT = auto()
    """内部統制報告書"""
    AMENDED_INTERNAL_CONTROL_REPORT = auto()
    """訂正内部統制報告書"""
    MATERIAL_EVENT_REPORT = auto()
    """臨時報告書"""
    PARENT_COMPANY_REPORT = auto()
    """親会社等状況報告書"""
    SHARE_REPURCHASE_REPORT = auto()
    """自己株券買付状況報告書"""
    AMENDED_SHARE_REPURCHASE_REPORT = auto()
    """訂正自己株券買付状況報告書"""


class TargetDocument:
    doc_id: str
    format_type: FormatType
    ticker: str
    doc_type: DocType


TargetPort = Union[EdinetTargetPort]

TargetConfig = Union[EdinetTargetConfig]
