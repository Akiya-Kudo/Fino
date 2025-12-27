from abc import ABC, abstractmethod
from datetime import date
from enum import Enum, IntEnum
from typing import Literal, TypedDict, Union


class EdinetFormatType(Enum):
    DOCUMENT = 1
    PDF = 2
    ATTACHMENT = 3
    ENGLISH = 4
    CSV = 5


class EdinetDocument(IntEnum):
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


class GetDocumentResultSet(TypedDict):
    count: int


class GetDocumentParam(TypedDict):
    date: Literal["YYYY-MM-DD"]
    type: str


class GetDocumentMetadata(TypedDict):
    title: str
    parameter: GetDocumentParam
    resultset: GetDocumentResultSet
    processDateTime: Literal["YYYY-MM-DD hh:mm"]
    status: str
    message: str


class GetDocumentDocs(TypedDict):
    seqNumber: int
    docID: str
    edinetCode: Union[None, str]
    secCode: Union[None, str]
    JCN: Union[None, str]
    filerName: Union[None, str]
    fundCode: Union[None, str]
    ordinanceCode: Union[None, str]
    formCode: Union[None, str]
    docTypeCode: Union[None, str]
    periodStart: Union[None, Literal["YYYY-MM-DD"]]
    periodEnd: Union[None, Literal["YYYY-MM-DD"]]
    submitDateTime: Literal["YYYY-MM-DD hh:mm"]
    docDescription: Union[None, str]
    issuerEdinetCode: Union[None, str]
    subjectEdinetCode: Union[None, str]
    subsidiaryEdinetCode: Union[None, str]
    currentReportReason: Union[None, str]
    parentDocID: Union[None, str]
    opeDateTime: Union[None, Literal["YYYY-MM-DD hh:mm"]]
    withdrawalStatus: Literal["0", "1", "2"]
    docInfoEditStatus: Literal["0", "1", "2"]
    disclosureStatus: Literal["0", "1", "2", "3"]
    xbrlFlag: Literal["0", "1"]
    pdfFlag: Literal["0", "1"]
    attachDocFlag: Literal["0", "1"]
    englishDocFlag: Literal["0", "1"]
    csvFlag: Literal["0", "1"]
    legalStatus: Literal["0", "1", "2"]


class GetDocumentResponse(TypedDict):
    metadata: GetDocumentMetadata


class GetDocumentResponseWithDocs(TypedDict):
    metadata: GetDocumentMetadata
    results: list[GetDocumentDocs]


class EdinetError(Exception):
    """Edinet APIの例外の基底クラス"""

    pass


class ResponseNot200Error(EdinetError):
    """EDINET API レスポンスが200ではない時に投げられる"""

    pass


class BadRequestError(ResponseNot200Error):
    """EDINET API 400エラー、リクエストパラメータになにか問題があると投げられる"""

    pass


class InvalidAPIKeyError(ResponseNot200Error):
    """EDINET API 401エラー、APIキーが無効だと投げられる"""

    pass


class ResourceNotFoundError(ResponseNot200Error):
    """EDINET API 404エラー、データが無いと投げられる"""

    pass


class InternalServerError(ResponseNot200Error):
    """EDINET API 500エラー、鯖側がおかしいと投げられる"""

    pass


class Edinet(ABC):
    api_key: str

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    @abstractmethod
    def get_document_list(
        self, date: date, withdocs: bool = False
    ) -> GetDocumentResponse | GetDocumentResponseWithDocs: ...

    @abstractmethod
    def get_document(self, doc_id: str, doc_type: EdinetDocument) -> bytes: ...
