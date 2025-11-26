import os

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.parser import event_parser
import schema as schemas

# ENVIRONMENT VARIABLES
table_endpoint = os.environ.get("INGESTION_STATE_TABLE_ENDPOINT")
table_name = os.environ.get("INGESTION_STATE_TABLE_NAME")

# INITIALIZATION
dynamodb = boto3.resource("dynamodb", endpoint_url=table_endpoint)
table = dynamodb.Table(table_name)

logger = Logger()

@logger.inject_lambda_context(log_event=True)
@event_parser(model=schemas.InputEvent)
def handler(event: schemas.InputEvent, context: LambdaContext) -> schemas.OutputEvent:
    """
    # Edinet Document ID Register Lambda Function

    ## Description
    - eventから書類IDを取得し、DynamoDBのIngestion Stateに登録する
        - PK: edinet/<sec_code>
        - Sort Key: document_id
    - すでにレコードが存在する場合は、更新を加えない
    """

    # Event Extract
    detail = event.detail
    document_ids = detail.document_ids
    sec_code = detail.sec_code


    # Generate Partition Key
    partition_key = f"edinet/{sec_code}"

    saved_count = 0
    for document_id in document_ids:
        table.put_item(
            Item={
                "data_source_group": partition_key,
                "document_id": document_id,
                "ingestion_state": "READY",
            }
        )
        saved_count += 1
        logger.info(f"SUCCESS SAVE DOCUMENT ID: PK: {partition_key}, SK: {document_id}")

    logger.info(f"SAVED COUNT: {saved_count}")
    return {
        "statusCode": 200,
        "body": {
            "message": "Success",
            "document_ids": document_ids,
            "sec_code": sec_code,
            "saved_count": len(saved_count),
        },
    }
