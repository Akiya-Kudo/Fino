from abc import ABC, abstractmethod
from typing import Protocol

from fino_core.collector.domain.entity.document import Document
from fino_core.collector.domain.value import DocumentId, DocumentType


class DocumentSourceCriteria(Protocol):
    """文書取得条件のプロトコル

    各データソースは、このプロトコルを実装した独自のCriteriaクラスを定義します。
    例: EdinetCriteria, TdnetCriteria

    このプロトコルは、application層で定義される具体的なCriteriaクラスが
    実装すべきインターフェースを表します。
    """

    pass


class DocumentSource(ABC):
    """外部データソースから文書を取得する抽象インターフェース

    このポートは、Aggregate Root（Document）のみを返します。
    メタデータのみの状態も、resource=NoneのDocumentとして扱います。

    このインターフェースは、EDINETやTDnetなどの具体的なデータソースに依存しません。
    実装はinfrastructure層で行われます。
    """

    @abstractmethod
    def get_document_list(self, criteria: DocumentSourceCriteria) -> list[Document]:
        """指定された条件に基づいて文書メタデータのリストを取得する

        メタデータのみの状態（resource=None）のDocumentのリストを返します。
        各Documentは、後でget_document()を使用して完全な状態にできます。

        Args:
            criteria: 文書取得の条件（ソース固有の実装）

        Returns:
            メタデータのみの状態のDocumentのリスト（resource=None）
        """
        ...

    @abstractmethod
    def get_document(self, document_id: DocumentId, document_type: DocumentType) -> Document:
        """指定された文書IDの完全なDocumentを取得する

        Args:
            document_id: 文書ID
            document_type: 開示種別

        Returns:
            完全な状態のDocument（resourceが設定されている）
        """
        ...
