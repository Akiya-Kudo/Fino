"""Application layer for collecting EDINET documents."""

from datetime import date
from typing import cast

from fino_core.domain.edinet import Edinet, EdinetDocument, GetDocumentResponseWithDocs
from fino_core.domain.period import Period
from fino_core.domain.storage import StoragePort


def collect_edinet(
    period: Period,
    storage: StoragePort,
    edinet: Edinet,
    doc_types: list[EdinetDocument] | EdinetDocument | None = None,
) -> None:
    """
    Collect EDINET documents for the specified period.

    Args:
        period: Period to collect documents for
        storage: Storage port implementation to save documents
        edinet: Edinet port implementation to fetch documents
        doc_types: Optional filter for document types to collect.
                   If None, collects all document types.
    """
    # Convert single doc_type to list for uniform processing
    if doc_types is None:
        doc_type_list: list[EdinetDocument] | None = None
    elif isinstance(doc_types, EdinetDocument):
        doc_type_list = [doc_types]
    elif isinstance(doc_types, list) and len(doc_types) == 0:
        # Empty list means collect all document types
        doc_type_list = None
    else:
        doc_type_list = doc_types

    for date_obj in period.iterate_by_day():
        document_list_response = edinet.get_document_list(date_obj, withdocs=True)
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

            # Filter by doc_types if specified
            if doc_type_list is not None and doc_type not in doc_type_list:
                continue

            document_bytes = edinet.get_document(doc_id, doc_type)
            storage.save(key=f"edinet/{doc_id}", data=document_bytes)
