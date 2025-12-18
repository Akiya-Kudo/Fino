from typing import Optional

from fino_core.model.disclosure_source_type import DocumentSourceType
from fino_core.model.doc_type import DocType
from fino_core.model.storage_type import StorageType
from pydantic import BaseModel, Field, model_validator


class PeriodInput(BaseModel):
    year: int = Field(ge=1900, le=3000, frozen=True)
    month: Optional[int] = Field(ge=1, le=12, frozen=True)
    day: Optional[int] = Field(ge=1, le=31, frozen=True)

    @model_validator(mode="after")
    def validate_period(cls, data: "PeriodInput") -> "PeriodInput":
        if data.day is not None and data.month is None:
            raise ValueError("month must be specified when day is specified")
        return data.model_dump()


class StorageInput(BaseModel):
    type: StorageType
    path: Optional[str] = Field(default="")
    storage_uri: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None


class DocumentSourceInput(BaseModel):
    type: DocumentSourceType
    api_key: str


class CollectDocumentInput(BaseModel):
    period: PeriodInput
    storage: StorageInput
    target: DocumentSourceInput
    doc_type: list[DocType] | DocType
