from dataclasses import dataclass
from datetime import datetime
from typing import Literal, overload

from fino_core._model.target.main import TargetPort, TargetType

from .response import GetDocumentResponse, GetDocumentResponseWithDocs


@dataclass
class EdinetTargetConfig:
    type: TargetType = TargetType.EDINET
    api_key: str


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
