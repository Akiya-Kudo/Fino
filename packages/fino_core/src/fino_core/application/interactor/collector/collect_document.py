from fino_core.application.input.collector import CollectorCollectDocumentInputDTO
from fino_core.application.output.collector import CollectorCollectDocumentOutputDTO


class CollectDocumentUseCase:
    """文書収集・ビジネスロジック"""

    def execute(self, input: CollectorCollectDocumentInputDTO) -> CollectorCollectDocumentOutputDTO:
        document_metadata_list = []

        return CollectorCollectDocumentOutputDTO(document_metadata_list=[])
