import datetime

from fino_core.factory.storage.main import create_storage
from fino_core.model.storage.main import StorageConfig


# TODO: targetが増えたら、Strategyパターンとかを採用して、処理の呼び出しと、分岐を分離する
# https://zenn.dev/lambdaphi/articles/strategy_factory_example
def collect(
    target_api_key: str,
    date: datetime.datetime,
    storage_path: str,
) -> None:
    print("collect edinet documents")
    storage = create_storage(StorageConfig(storage_path=storage_path))
    storage.save(storage)
