from dataclasses import dataclass

from fino_core.domain.entity.document_metadata import DocumentMetadata


@dataclass
class CollectorCollectDocumentOutputDTO:
    document_metadata_list: list[DocumentMetadata]
