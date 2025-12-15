import datetime
from typing import Any, Literal, Union, overload

import requests

from .exception import (
    BadRequestError,
    InternalServerError,
    InvalidAPIKeyError,
    ResourceNotFoundError,
    ResponseNot200Error,
)
from .response import (
    GetDocumentResponse,
    GetDocumentResponseWithDocs,
)

__all__ = ["Edinet"]


class Edinet:
    # EDINET API Version (今のところ2しかないけど)
    api_version: int = 2
    base_url: str = "https://api.edinet-fsa.go.jp/api/v{self.api_version}/"
    api_key: str

    def __init__(self, api_key: str) -> None:
        self.api_version = 2
        # apiの保存
        self.api_key = api_key
        # edinetAPIのURL
        self.base_url = f"https://api.edinet-fsa.go.jp/api/v{self.api_version}/"

    def __request(self, endpoint: str, params: dict[str, Any]) -> requests.Response:
        """内部で使うrequestsメソッド、getリクエストのみ。"""

        params["Subscription-Key"] = self.__token

        res = requests.get(
            url=self.__EDINET_URL + endpoint,
            params=params,
            timeout=(3.0, 7.5),  # timeout: (connect timeout, read timeout)
        )

        if res.status_code == 200:
            return res
        elif res.status_code == 400:
            raise BadRequestError(
                res.status_code, res.text
            )  # 例外のargはすべて右の通り: int(statuscode), str(text)
        elif res.status_code == 401:
            raise InvalidAPIKeyError(res.status_code, res.text)
        elif res.status_code == 404:
            raise ResourceNotFoundError(res.status_code, res.text)
        elif res.status_code == 500:
            raise InternalServerError(res.status_code, res.text)
        else:
            raise ResponseNot200Error(res.status_code, res.text)

    @overload
    def get_document_list(
        self, date: datetime.datetime, withdocs: False
    ) -> GetDocumentResponse: ...
    @overload
    def get_document_list(
        self, date: datetime.datetime, withdocs: True
    ) -> GetDocumentResponseWithDocs: ...
    @overload
    def get_document_list(self, date: datetime.datetime) -> GetDocumentResponse: ...

    def get_document_list(
        self, date: datetime.datetime, withdocs: bool = False
    ) -> Union[GetDocumentResponse, GetDocumentResponseWithDocs]:
        """
        `documents.json`エンドポイントのラッパー

        Parameters
        ----------
        date: datetime.datetime
            `datetime.datetime`オブジェクト、年月日の指定。
        withdocs: :obj:`bool`, default False
            提出書類一覧を含めるか、デフォルトは含めない。
        """
        if isinstance(date, datetime.datetime) and isinstance(
            withdocs, bool
        ):  # 引数があっているか確認
            params = {
                "date": date.strftime("%Y-%m-%d"),
                "type": (withdocs + 1),  # boolはintのサブクラス
            }

            response = self.__request(endpoint="documents.json", params=params)

            return response.json()

        else:
            raise ValueError()

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
        if isinstance(doc_id, str) and type in (1, 2, 3, 4, 5):
            params = {"type": type}

            response = self.__request(endpoint=f"documents/{doc_id}", params=params)

            return response.content

        else:
            raise ValueError()


# Based on code from https://github.com/35enidoi/edinet_wrap
# Licensed under the Apache License, Version 2.0
# Copyright 2024 35enidoi
