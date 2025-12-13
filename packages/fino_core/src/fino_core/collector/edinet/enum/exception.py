class EdinetException(Exception):
    """Edinetの例外の基底クラス"""

    pass


class ResponseNot200(EdinetException):
    """レスポンスが200ではない時に投げられる"""

    pass


class BadRequest(ResponseNot200):
    """400エラー、リクエストパラメータになにか問題があると投げられる"""

    pass


class InvalidAPIKey(ResponseNot200):
    """401エラー、APIキーが無効だと投げられる"""

    pass


class ResourceNotFound(ResponseNot200):
    """404エラー、データが無いと投げられる"""

    pass


class InternalServerError(ResponseNot200):
    """500エラー、鯖側がおかしいと投げられる"""

    pass


# Based on code from https://github.com/35enidoi/edinet_wrap
# Licensed under the Apache License, Version 2.0
# Copyright 2024 35enidoi
