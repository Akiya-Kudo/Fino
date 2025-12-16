from typing import List

from fino_core._factory.storage import create_storage
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

    # set storage
    storage = create_storage(input.storage)
    print(storage)
