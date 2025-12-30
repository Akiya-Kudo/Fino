from dataclasses import dataclass


@dataclass(frozen=True)
class CollectEdinetDocumentController:
    repository: DocumentRepository
    usecase: CollectEdinetDOcumentUsecase

    def execute() -> :
        return usecase.execute()
