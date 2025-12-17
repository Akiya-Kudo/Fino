from dataclasses import dataclass
from datetime import date
from enum import Enum


class DisclosureCategory(Enum):
    ANNUAL = "annual"
    QUARTERLY = "quarterly"
    EVENT = "event"


@dataclass(frozen=True)
class DisclosureDocument:
    """
    開示書類という業務概念（制度非依存）
    """

    source: str
    category: DisclosureCategory
    document_id: str
    company_code: str
    period_end: date
    disclosed_at: date
