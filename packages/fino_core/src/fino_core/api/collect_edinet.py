"""Public API for collecting EDINET documents."""

from dataclasses import asdict
from typing import Optional, Self, cast

from fino_core.application.collector.collect_edinet import collect_edinet as _collect_edinet
from fino_core.application.dto.edinet_doc_type import EdinetDocTypeDto
from fino_core.application.dto.query_period import QueryPeriod
from fino_core.domain.edinet import EdinetDocType
from fino_core.domain.storage_type import StorageType
from fino_core.infrastructure.edinet import create_edinet
from fino_core.infrastructure.storage import create_storage
from pydantic import BaseModel, Field, model_validator


class PeriodInput(BaseModel):
    """Input model for period specification."""

    year: int = Field(ge=1900, le=3000, frozen=True)
    month: Optional[int] = Field(ge=1, le=12, frozen=True)
    day: Optional[int] = Field(ge=1, le=31, frozen=True)

    @model_validator(mode="after")
    def validate_period(self) -> Self:
        if self.day is not None and self.month is None:
            raise ValueError("month must be specified when day is specified")
        return self


class StorageConfigInput(BaseModel):
    """Input model for storage configuration."""

    type: StorageType
    path: Optional[str] = Field(default="")
    storage_uri: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    bucket: Optional[str] = None
    api_key: Optional[str] = None
    region: Optional[str] = None


class CollectDocumentInput(BaseModel):
    """Input model for collecting EDINET documents."""

    period: PeriodInput
    storage: StorageConfigInput
    doc_type: list[EdinetDocType] | EdinetDocType | None = None
    api_key: str


class CollectEdinetInput(BaseModel):
    """Input model for collecting EDINET documents."""

    period: PeriodInput
    storage: StorageConfigInput
    doc_types: list[int] | int | list[EdinetDocType] | EdinetDocType = EdinetDocType.ANNUAL_REPORT
    api_key: str


def collect_edinet(input: CollectEdinetInput) -> None:
    # Convert input period to query period
    period = QueryPeriod.from_values(values=asdict(input.period))

    # Convert doc_type to Dto
    doc_types_dto = EdinetDocTypeDto(
        doc_types=cast(
            list[int], input.doc_types
        )  # validatorでnormalizeされ、list[int]になる想定のためcastで型を強制する
    )

    # Create infrastructure implementations using factory functions
    storage = create_storage(input.storage)
    edinet = create_edinet(api_key=input.api_key)

    # Call application layer function with injected dependencies
    _collect_edinet(
        period=period,
        storage=storage,
        edinet=edinet,
        doc_types=doc_types_dto.to_domain(),
    )


__all__ = ["collect_edinet", "CollectDocumentInput", "PeriodInput", "StorageConfigInput"]
