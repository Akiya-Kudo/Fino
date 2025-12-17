import datetime
from typing import Any, Literal, Union

import requests
from fino_core._model.target.edinet import (
    BadRequestError,
    EdinetTargetConfig,
    EdinetTargetPort,
    GetDocumentResponse,
    GetDocumentResponseWithDocs,
    InternalServerError,
    InvalidAPIKeyError,
    ResourceNotFoundError,
    ResponseNot200Error,
)


class EdinetAdapter(EdinetTargetPort):
    # EDINET API Version (今のところ2しかないけど)
    api_version: int = 2
    base_url: str = "https://api.edinet-fsa.go.jp/api/v{self.api_version}/"
    api_key: str

    def __init__(self, config: EdinetTargetConfig) -> None:
        super(config)
        self.api_version = 2
        # apiの保存
        self.api_key = config.api_key
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

    def get_document_list(
        self, date: datetime.datetime, withdocs: bool = False
    ) -> Union[GetDocumentResponse, GetDocumentResponseWithDocs]:
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
        response = self.__request(endpoint=f"documents/{doc_id}", params={"type": type})

        return response.content


# Based on code from https://github.com/35enidoi/edinet_wrap
# Licensed under the Apache License, Version 2.0
# Copyright 2024 35enidoi
