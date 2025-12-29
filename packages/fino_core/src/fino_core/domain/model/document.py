from dataclasses import dataclass
from enum import Enum


class FilingFormat(Enum):
    PDF = "pdf"
    XBRL = "xbrl"
    CSV = "csv"


@dataclass
class Document:
    document_id: str
    name: str
    filing_format: FilingFormat
    resource: bytes | None = None
