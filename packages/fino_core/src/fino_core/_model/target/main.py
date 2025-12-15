from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TargetType(str, Enum):
    EDINET = "edinet"


@dataclass
class TargetConfig:
    type: TargetType
    api_key: str | None = None


class TargetPort(ABC):
    @abstractmethod
    def get_document_list(self, date: datetime) -> list[str]: ...
    @abstractmethod
    def get_document(self, doc_id: str) -> bytes: ...
