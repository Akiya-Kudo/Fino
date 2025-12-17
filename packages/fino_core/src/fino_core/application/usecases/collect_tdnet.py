"""Use case for collecting TDNET disclosures."""

from typing import List

from fino_core._factory.storage import create_storage
from fino_core.domain import Document

from .input import CollectTdnetInput
from .output import CollectTdnetOutput


def collect_tdnet(input: CollectTdnetInput) -> CollectTdnetOutput:
    """
    TDNET適時開示情報を収集するUseCase

    業務的に違うなら UseCase も違う。
    無理に統合せず、明示的に分離する。

    Note: TDNETの実装は今後追加予定
    """
    # TODO: TDNETの実装を追加
    # initialize storage
    storage = create_storage(input.storage)

    # collect documents
    documents: List[Document] = []

    # TDNETの実装が完了するまで空のリストを返す
    return CollectTdnetOutput(documents=documents)
