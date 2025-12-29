from datetime import datetime
from typing import Literal, Union

DataSourceType = Literal["edinet", "tdnet"]
StorageType = Literal["local", "s3"]


class Collector:
    """
    パッケージ利用者向けの公開API

    Usage:
        collector = Collector(
            data_source="edinet",
            storage="s3",
            data_source_config={"api_key": "your_key"},
            storage_config={"bucket_name": "your-bucket"}
        )

        result = collector.collect(
            start_date="2024-01-01",
            end_date="2024-01-31",
            company_codes=["1234", "5678"]
        )
    """

    def __init__(
        self,
        data_source: DataSourceType,
        storage: StorageType,
        data_source_config: dict,
        storage_config: dict,
    ) -> None:
        # ファクトリーパターンでインスタンス生成
        self._data_source = self._create_data_source(data_source, data_source_config)
        self._storage = self._create_storage(storage, storage_config)
        self._usecase = CollectUseCase(self._data_source, self._storage)

    def collect(
        self,
        start_date: Union[str, date],
        end_date: Union[str, date],
        company_codes: Optional[List[str]] = None,
        storage_path: str = "documents",
    ) -> dict:
        """
        文書を収集してストレージに保存

        Returns:
            dict: {"success": bool, "collected_count": int, "saved_paths": list, "errors": list}
        """
        # 日付変換
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # DTO作成
        input_dto = CollectInputDTO(
            start_date=start_date,
            end_date=end_date,
            company_codes=company_codes,
            storage_path=storage_path,
        )

        # UseCase実行
        output_dto = self._usecase.execute(input_dto)

        # 辞書に変換して返却
        return {
            "success": output_dto.success,
            "collected_count": output_dto.collected_count,
            "saved_paths": output_dto.saved_paths,
            "errors": output_dto.errors,
        }

    @staticmethod
    def _create_data_source(source_type: DataSourceType, config: dict) -> DataSourceRepository:
        """データソースのファクトリーメソッド"""
        if source_type == "edinet":
            return EdinetDataSource(api_key=config["api_key"])
        elif source_type == "tdnet":
            return TdnetDataSource(credentials=config)
        else:
            raise ValueError(f"Unknown data source: {source_type}")

    @staticmethod
    def _create_storage(storage_type: StorageType, config: dict) -> StorageRepository:
        """ストレージのファクトリーメソッド"""
        if storage_type == "local":
            return LocalStorage(base_path=config.get("base_path", "./data"))
        elif storage_type == "s3":
            return S3Storage(
                bucket_name=config["bucket_name"], region=config.get("region", "ap-northeast-1")
            )
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")
