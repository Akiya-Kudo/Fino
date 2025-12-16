import datetime
from datetime import date
from typing import List

from fino_core._factory.storage import create_storage
from fino_core._factory.target import create_target
from fino_core._model.period import Period
from fino_core._model.storage import StorageConfig
from fino_core._model.target import TargetConfig
from fino_core._model.target.edinet import EdinetDoc
from pydantic import BaseModel, field_validator


class CollectInput(BaseModel):
    target: TargetConfig
    period: Period
    storage: StorageConfig
    doc_type: EdinetDoc | list[EdinetDoc]

    @field_validator("period", mode="before")
    def validate_period(self, v: Period) -> Period:
        """
        指定範囲が未来の場合はエラーを返す
        """
        if v.closest_day > date.now():
            raise ValueError("period must be in the past.")

        return v

    @field_validator("doc_type", mode="before")
    def validate_doc_type(self, v: EdinetDoc | list[EdinetDoc]) -> list[EdinetDoc]:
        """
        - 単数 → list に変換
        - 空リストは禁止
        """
        if isinstance(v, list):
            if len(v) == 0:
                raise ValueError("doc_type must contain at least one item")
            return v

        # 単数指定
        return [v]


class CollectOutput(BaseModel):
    documents: List[str]


# TODO: targetが増えたら、Strategyパターンとかを採用して、処理の呼び出しと、分岐を分離する
# https://zenn.dev/lambdaphi/articles/strategy_factory_example
def collect(input: CollectInput) -> CollectOutput:
    # input
    doc_type = input.doc_type
    if isinstance(doc_type, list):
        doc_type = doc_type[0]
    else:
        doc_type = [doc_type]

    # set target
    target = create_target(input.target)
    print(target)

    # set storage
    storage = create_storage(input.storage)
    print(storage)

    documents: List[str] = []
    for date_obj in input.period.iterate_by_day():
        # dateをdatetimeに変換（時刻は00:00:00）
        datetime_obj = datetime.datetime.combine(date_obj, datetime.time.min)
        # target.get_document_list()を呼び出し
        document_list = target.get_document_list(datetime_obj, withdocs=True)
        # TODO: document_listからdocIDを抽出してdocumentsに追加

    return CollectOutput(documents=documents)
