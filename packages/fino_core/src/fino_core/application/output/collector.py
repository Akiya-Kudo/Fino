from dataclasses import dataclass

from fino_core.domain.model.document.document_metadata import DocumentMetadata


@dataclass
class CollectorCollectDocumentOutputDTO:
    document_metadata_list: list[DocumentMetadata]
