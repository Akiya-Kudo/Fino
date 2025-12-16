from dataclasses import dataclass
from datetime import datetime
from enum import Enum, IntEnum
from typing import Literal, overload

from fino_core._model.target.main import TargetPort, TargetType

from .response import GetDocumentResponse, GetDocumentResponseWithDocs


@dataclass
class EdinetTargetConfig:
    type: TargetType = TargetType.EDINET
    api_key: str


class EdinetDoc(IntEnum):
    """
    EDINET 書類種別コード（ファンダメンタルズ分析向け）

    value: EDINETコード
    name : 英語識別子（用途別に整理）
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
    INTERNAL_CONTROL_REPORT = 235
    """内部統制報告書"""
    AMENDED_INTERNAL_CONTROL_REPORT = 236
    """訂正内部統制報告書"""
    MATERIAL_EVENT_REPORT = 180
    """臨時報告書"""
    PARENT_COMPANY_REPORT = 200
    """親会社等状況報告書"""
    SHARE_REPURCHASE_REPORT = 220
    """自己株券買付状況報告書"""
    AMENDED_SHARE_REPURCHASE_REPORT = 230
    """訂正自己株券買付状況報告書"""


class EdinetFormatType(Enum):
    DOCUMENT = 1
    PDF = 2
    ATTACHMENT = 3
    ENGLISH = 4
    CSV = 5


class EdinetTargetPort(TargetPort):
    def __init__(self, config: EdinetTargetConfig) -> None:
        self.api_key = config.api_key

    @overload
    def get_document_list(
        self, date: datetime.datetime, withdocs: False
    ) -> GetDocumentResponse: ...
    @overload
    def get_document_list(
        self, date: datetime.datetime, withdocs: True
    ) -> GetDocumentResponseWithDocs: ...
    def get_document_list(self, date: datetime.datetime) -> GetDocumentResponse:
        """
        `documents.json`エンドポイントのラッパー

        Parameters
        ----------
        date: datetime.datetime
            `datetime.datetime`オブジェクト、年月日の指定。
        withdocs: :obj:`bool`, default False
            提出書類一覧を含めるか、デフォルトは含めない。
        """
        ...

    def get_document(self, doc_id: str, type: Literal[1, 2, 3, 4, 5]) -> bytes:
        """
        ドキュメントの取得

        Parameters
        ----------
        doc_id: str
            書類管理番号
        type: Literal[1, 2, 3, 4, 5]
            - 1: 提出本文書及び監査報告書、XBRLを取得
            - 2: PDFを取得
            - 3: 代替書面・添付文書を取得
            - 4: 英文ファイルを取得
            - 5: CSVを取得
        """
        ...
