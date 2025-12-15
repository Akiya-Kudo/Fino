import datetime

from fino_core._factory.storage.factory import create_storage


# TODO: targetが増えたら、Strategyパターンとかを採用して、処理の呼び出しと、分岐を分離する
# https://zenn.dev/lambdaphi/articles/strategy_factory_example
def collect(
    api_key: str,
    date: datetime.datetime,
    storage_path: str,
) -> None:
    print("collect edinet documents")
    storage = create_storage(storage_path)
    storage.save(storage)
