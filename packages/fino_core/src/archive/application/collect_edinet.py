"""Use case for collecting EDINET documents."""

from typing import List

from fino_core._factory.storage import create_storage
from fino_core._factory.target import create_target
from fino_core.domain import DisclosureSource, Document, DocumentClassification
from fino_core.domain.document_type import EdinetDocumentType

from .input import CollectEdinetInput
from .output import CollectEdinetOutput


def collect_edinet(input: CollectEdinetInput) -> CollectEdinetOutput:
    """
    EDINET書類を収集するUseCase

    業務的に違うなら UseCase も違う。
    無理に統合せず、明示的に分離する。
    """
    # input validation
    if isinstance(input.doc_types, list):
        doc_types = input.doc_types
    elif isinstance(input.doc_types, EdinetDocumentType):
        doc_types = [input.doc_types]
    else:
        raise ValueError("Invalid doc_types")

    # initialize target and storage
    from fino_core._model.target.edinet import EdinetTargetConfig

    target_config = EdinetTargetConfig(api_key=input.api_key)
    target = create_target(target_config)
    storage = create_storage(input.storage)

    # collect documents
    documents: List[Document] = []
    for i_date in input.period.iterate_by_day():
        list_response = target.get_document_list(i_date, withdocs=True)
        document_list = list_response["results"]
        for document in document_list:
            # EDINET書類種別コードを取得
            doc_type_code = document.get("docTypeCode")
            if doc_type_code is None:
                continue

            # EDINET書類種別コードをEdinetDocumentTypeに変換
            try:
                edinet_doc_type = EdinetDocumentType(doc_type_code)
            except ValueError:
                # 未知の書類種別はスキップ
                continue

            # 指定された書類種別に一致するかチェック
            if edinet_doc_type not in doc_types:
                continue

            # 書類を取得
            doc_bytes = target.get_document(document["docID"], edinet_doc_type)
            storage.save(doc_bytes, path=f"edinet/{document['docID']}")

            # Domainエンティティを作成
            classification = DocumentClassification.from_edinet(edinet_doc_type)
            domain_document = Document(
                id=document["docID"],
                source=DisclosureSource.EDINET,
                classification=classification,
                ticker=document.get("secCode"),
                format_type=None,  # TODO: フォーマット情報を追加
            )
            documents.append(domain_document)

    return CollectEdinetOutput(documents=documents)
