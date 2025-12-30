"""Public API Provider"""


def collect_edinet_document(input: Any):
    """collect edinet document"""

    repository = DocumentRepository
    usecase = CollectEdinetDocumentUsecase(repository)
    controller = CollectEdinetDocumentController(usecase)
    return controller(input)
