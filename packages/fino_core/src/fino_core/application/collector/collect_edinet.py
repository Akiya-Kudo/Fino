from dataclasses import asdict
from typing import Optional, Self, cast

from fino_core.factory.data_source import create_edinet
from fino_core.factory.storage import create_storage
from fino_core.model.edinet import EdinetDocument, GetDocumentResponseWithDocs
from fino_core.model.period import Period
from fino_core.model.storage_type import StorageType
from pydantic import BaseModel, Field, model_validator


class PeriodInput(BaseModel):
    year: int = Field(ge=1900, le=3000, frozen=True)
    month: Optional[int] = Field(ge=1, le=12, frozen=True)
    day: Optional[int] = Field(ge=1, le=31, frozen=True)

    @model_validator(mode="after")
    def validate_period(self) -> Self:
        if self.day is not None and self.month is None:
            raise ValueError("month must be specified when day is specified")
        return self


class StorageConfigInput(BaseModel):
    type: StorageType
    path: Optional[str] = Field(default="")
    storage_uri: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    bucket: Optional[str] = None
    api_key: Optional[str] = None
    region: Optional[str] = None


class CollectDocumentInput(BaseModel):
    period: PeriodInput
    storage: StorageConfigInput
    doc_type: list[EdinetDocument] | EdinetDocument
    api_key: str


def collect_edinet(input: CollectDocumentInput) -> None:
    period = Period.from_values(values=asdict(input.period))
    storage = create_storage(input.storage)
    edinet = create_edinet(api_key=input.api_key)

    for date in period.iterate_by_day():
        document_list_response = edinet.get_document_list(date, withdocs=True)
        document_list = cast(GetDocumentResponseWithDocs, document_list_response)
        for document in document_list["results"]:
            doc_id = document["docID"]
            doc_type_code = document.get("docTypeCode")
            if doc_type_code is None:
                continue
            try:
                doc_type = EdinetDocument(doc_type_code)
            except ValueError:
                continue
            document_bytes = edinet.get_document(doc_id, doc_type)
            storage.save(key=f"edinet/{doc_id}", data=document_bytes)
