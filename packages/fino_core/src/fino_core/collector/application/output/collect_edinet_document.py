from dataclasses import dataclass


@dataclass
class CollectEdinetDocumentOutput:
    """文書収集の出力DTO

    メタデータのみの状態（resource=None）のDocumentのリストを含みます。
    各Documentは、後で完全な状態にできます。
    """

    document_list: list[Document]
