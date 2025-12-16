from typing import List

from fino_core._factory.storage import create_storage
from fino_core._factory.target import create_target
from fino_core._model.target.edinet import EdinetDoc
from fino_core._model.target.main import TargetDocument

from .input import CollectInput
from .output import CollectOutput


# TODO: targetが増えたら、Strategyパターンとかを採用して、処理の呼び出しと、分岐を分離する
# https://zenn.dev/lambdaphi/articles/strategy_factory_example
def collect(input: CollectInput) -> CollectOutput:
    # input validation
    if isinstance(input.doc_type, list):
        doc_types = input.doc_type
    elif isinstance(input.doc_type, EdinetDoc):
        doc_types = [input.doc_type]
    else:
        raise ValueError("Invalid doc_type")

    # initialize target and storage
    target = create_target(input.target)
    storage = create_storage(input.storage)

    # collect documents
    doc_bytes_list: List[bytes] = []
    doc_output_list: list[TargetDocument] = []
    for i_date in input.period.iterate_by_day():
        list_response = target.get_document_list(i_date, withdocs=True)
        document_list = list_response["results"]
        for document in document_list:
            if document["docTypeCode"] not in doc_types:
                continue
            doc_bytes = target.get_document(document["docID"], document["docTypeCode"])
            storage.save(doc_bytes)
            doc_output_list.append(doc_bytes)

    return CollectOutput(documents=doc_bytes_list)
