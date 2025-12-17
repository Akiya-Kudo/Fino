"""Output models for use cases."""

from pydantic import BaseModel

from fino_core.domain import Document


class CollectEdinetOutput(BaseModel):
    """EDINET書類収集の出力"""

    documents: list[Document]
    """収集された書類のリスト"""


class CollectTdnetOutput(BaseModel):
    """TDNET適時開示情報収集の出力"""

    documents: list[Document]
    """収集された開示情報のリスト"""
