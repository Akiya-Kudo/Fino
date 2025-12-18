from fino_core._application.collector.port.edinet import EdinetDisclosurePort
from fino_core._application.collector.query.edinet import EdinetDateQuery
from fino_core._domain.document.document import DisclosureDocument


class CollectEdinetDocuments:
    def __init__(self, port: EdinetDisclosurePort) -> None:
        self._port = port

    def execute(self, query: EdinetDateQuery) -> list[DisclosureDocument]:
        return list(self._port.list_documents(query))
