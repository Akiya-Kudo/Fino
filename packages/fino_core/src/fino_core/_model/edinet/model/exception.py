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


# Based on code from https://github.com/35enidoi/edinet_wrap
# Licensed under the Apache License, Version 2.0
# Copyright 2024 35enidoi
