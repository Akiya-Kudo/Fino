from fino_core._factory.storage import create_storage

from .interface import CollectInput, CollectOutput


# TODO: targetが増えたら、Strategyパターンとかを採用して、処理の呼び出しと、分岐を分離する
# https://zenn.dev/lambdaphi/articles/strategy_factory_example
def collect(input: CollectInput) -> CollectOutput:
    # set target

    # set storage
    storage = create_storage(input.storage)
    print(storage)
