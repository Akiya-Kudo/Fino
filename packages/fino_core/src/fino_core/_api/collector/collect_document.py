from datetime import date
from typing import Iterable

from fino_core._application.collector.collect_edinet_document import CollectEdinetDocuments
from fino_core._application.collector.query.edinet import EdinetDateQuery
from fino_core._domain.document.document import DisclosureDocument
from fino_core._infrastructure.collector.edinet.client import EdinetApiClient


def collect_documents(
    start_date: date,
    end_date: date,
) -> Iterable[DisclosureDocument]:
    adopter = EdinetApiClient()
    usecase = CollectEdinetDocuments(adopter)

    query = EdinetDateQuery(
        start_date=start_date,
        end_date=end_date,
    )

    return usecase.execute(query)
