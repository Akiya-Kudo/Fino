from enum import Enum, auto


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
