edinet_collector = DocumentCollecter(
    storage_config=StorageConfig(
        type=StorageType.LOCAL,
        path="./data",
    ),
    source=DisclosureSourceConfig(
        type=DisclosureSourceType.EDINET,
        api_key="1234567890",
    ),
)

saved_documents = edinet_collector.collect_document(
    timescope=TimeScope(year=2024, month=1),
    doc_types=[EdinetDocType.ANNUAL_REPORT],
)

edinet_collector = DocumentCollecter(
    storage_config=StorageConfig(
        type=StorageType.S3,
        storage_uri="s3://your-bucket/path",
    ),
    source=DisclosureSourceConfig(
        type=DisclosureSourceType.TDNET,
        username="your-username",
        password="your-password",
    ),
)

saved_documents = edinet_collector.collect_document(
    timescope=TimeScope(year=2024, month=1),
    doc_types=[EdinetDocType.ANNUAL_REPORT],
)
