from abc import ABC, abstractmethod
from typing import Iterable

from fino_core._application.collector.query.edinet import EdinetDateQuery
from fino_core._domain.document.document import DisclosureDocument


class EdinetDisclosurePort(ABC):
    """
    EDINET が提供する能力
    """

    @abstractmethod
    def list_documents(self, query: EdinetDateQuery) -> Iterable[DisclosureDocument]: ...
