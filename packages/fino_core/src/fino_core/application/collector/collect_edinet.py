from typing import Optional

from fino_core.factory.storage import create_storage
from fino_core.model.edinet import Edinet, EdinetDocument
from fino_core.model.period import Period
from fino_core.model.storage_type import StorageType
from pydantic import BaseModel, Field, model_validator


class PeriodInput(BaseModel):
    year: int = Field(ge=1900, le=3000, frozen=True)
    month: Optional[int] = Field(ge=1, le=12, frozen=True)
    day: Optional[int] = Field(ge=1, le=31, frozen=True)

    @model_validator(mode="after")
    def validate_period(self, data: "PeriodInput") -> "PeriodInput":
        if data.day is not None and data.month is None:
            raise ValueError("month must be specified when day is specified")
        return data.model_dump()


class StorageConfigInput(BaseModel):
    type: StorageType
    path: Optional[str] = Field(default="")
    storage_uri: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None


class CollectDocumentInput(BaseModel):
    period: PeriodInput
    storage: StorageConfigInput
    doc_type: list[EdinetDocument] | EdinetDocument
    api_key: str


def collect_documents(input: CollectDocumentInput) -> None:
    period = Period.from_input(input.period)
    storage = create_storage(input.storage_config)
    edinet = Edinet(api_key=input.api_key)
