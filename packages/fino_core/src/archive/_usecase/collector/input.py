from datetime import date

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
