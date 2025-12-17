"""Input models for use cases."""

from pydantic import BaseModel, field_validator

from fino_core._model.period import Period
from fino_core._model.storage import StorageConfig
from fino_core.domain.document_type import EdinetDocumentType, TdnetDocumentType


class CollectEdinetInput(BaseModel):
    """EDINET書類収集の入力"""

    period: Period
    storage: StorageConfig
    api_key: str
    doc_types: EdinetDocumentType | list[EdinetDocumentType]

    @field_validator("period", mode="before")
    def validate_period(self, v: Period) -> Period:
        """
        指定範囲が未来の場合はエラーを返す
        """
        from datetime import date

        if v.closest_day > date.now():
            raise ValueError("period must be in the past.")

        return v

    @field_validator("doc_types", mode="before")
    def validate_doc_types(
        self, v: EdinetDocumentType | list[EdinetDocumentType]
    ) -> list[EdinetDocumentType]:
        """
        - 単数 → list に変換
        - 空リストは禁止
        """
        if isinstance(v, list):
            if len(v) == 0:
                raise ValueError("doc_types must contain at least one item")
            return v

        # 単数指定
        return [v]


class CollectTdnetInput(BaseModel):
    """TDNET適時開示情報収集の入力"""

    period: Period
    storage: StorageConfig
    doc_types: TdnetDocumentType | list[TdnetDocumentType]

    @field_validator("period", mode="before")
    def validate_period(self, v: Period) -> Period:
        """
        指定範囲が未来の場合はエラーを返す
        """
        from datetime import date

        if v.closest_day > date.now():
            raise ValueError("period must be in the past.")

        return v

    @field_validator("doc_types", mode="before")
    def validate_doc_types(
        self, v: TdnetDocumentType | list[TdnetDocumentType]
    ) -> list[TdnetDocumentType]:
        """
        - 単数 → list に変換
        - 空リストは禁止
        """
        if isinstance(v, list):
            if len(v) == 0:
                raise ValueError("doc_types must contain at least one item")
            return v

        # 単数指定
        return [v]
