from dataclasses import dataclass

from fino_core.domain.entity.document import Document


@dataclass
class CollectorCollectDocumentOutputDTO:
    """文書収集の出力DTO

    メタデータのみの状態（resource=None）のDocumentのリストを含みます。
    各Documentは、後で完全な状態にできます。
    """

    document_list: list[Document]
