from dataclasses import dataclass

from fino_core.collector.application.input.collect_edinet_document import CollectEdinetDocumentInput
from fino_core.collector.application.output.collect_edinet_document import (
    CollectEdinetDocumentOutput,
)


@dataclass
class CollectEdinetDocumentUsecase:
    """Usecase: Collect Edinet Document"""

    def execute(self, input: CollectEdinetDocumentInput) -> CollectEdinetDocumentOutput: ...
