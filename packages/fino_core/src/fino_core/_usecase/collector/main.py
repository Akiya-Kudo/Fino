import datetime
from typing import List

from fino_core._factory.storage import create_storage
from fino_core._factory.target import create_target
from fino_core._model.period import Period
from fino_core._model.storage import StorageConfig
from fino_core._model.target import TargetConfig
from pydantic import BaseModel


class CollectInput(BaseModel):
    target: TargetConfig
    period: Period
    storage: StorageConfig


class CollectOutput(BaseModel):
    documents: List[str]


# TODO: targetが増えたら、Strategyパターンとかを採用して、処理の呼び出しと、分岐を分離する
# https://zenn.dev/lambdaphi/articles/strategy_factory_example
def collect(input: CollectInput) -> CollectOutput:
    # set target
    target = create_target(input.target)
    print(target)

    # set storage
    storage = create_storage(input.storage)
    print(storage)

    # get document list looping by period
    documents: List[str] = []
    for date_obj in input.period.iterate_by_day():
        # dateをdatetimeに変換（時刻は00:00:00）
        datetime_obj = datetime.datetime.combine(date_obj, datetime.time.min)
        # target.get_document_list()を呼び出し
        # TODO: 実際の実装に合わせて調整
        # 実装例:
        # response = target.get_document_list(datetime_obj, withdocs=False)
        # if response and "results" in response:
        #     for doc in response["results"]:
        #         documents.append(doc["docID"])
        # 現時点では未実装のため、datetime_objを使用しない
        _ = datetime_obj  # 実装時に削除

    return CollectOutput(documents=documents)
