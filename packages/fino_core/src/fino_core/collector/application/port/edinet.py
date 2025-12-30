from abc import ABC, abstractmethod
from datetime import date

from fino_core.domain.entity.document import Document
from fino_core.domain.value import DisclosureType


class EdinetRepository(ABC):
    """EDINETから文書を取得するポート（インターフェース）

    このポートは、Aggregate Root（Document）のみを返します。
    メタデータのみの状態も、resource=NoneのDocumentとして扱います。
    """

    @abstractmethod
    def get_document_list(self, date: date) -> list[Document]:
        """指定日の文書メタデータのリストを取得する

        メタデータのみの状態（resource=None）のDocumentのリストを返します。
        各Documentは、後でget_document()を使用して完全な状態にできます。

        Args:
            date: 取得する日付

        Returns:
            メタデータのみの状態のDocumentのリスト（resource=None）
        """
        ...

    @abstractmethod
    def get_document(self, doc_id: str, doc_type: DisclosureType) -> Document:
        """指定された文書IDの完全なDocumentを取得する

        Args:
            doc_id: 文書ID
            doc_type: 開示種別

        Returns:
            完全な状態のDocument（resourceが設定されている）
        """
        ...
