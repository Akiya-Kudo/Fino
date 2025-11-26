import os

import boto3
from boto3.dynamodb.conditions import Key
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

    # Get Existing Document IDs from DynamoDB
    result = table.query(
        KeyConditionExpression=Key("data_source_group").eq(partition_key)
    )

    # Extract Existing Document IDs & Get Document IDs for Save
    existing_document_ids = [item["document_id"] for item in result.get("Items", [])]
    document_ids_for_save = [document_id for document_id in document_ids if document_id not in existing_document_ids]

    # Save Document IDs to DynamoDB
    saved_document_ids = []
    for document_id in document_ids_for_save:
        table.put_item(
            Item={
                "data_source_group": partition_key,
                "document_id": document_id,
                "ingestion_state": "READY",
            }
        )
        saved_document_ids.append(document_id)
        logger.info(f"SUCCESS SAVE DOCUMENT ID: PK: {partition_key}, SK: {document_id}")

    logger.info(f"SAVED COUNT: {len(saved_document_ids)}")
    return {
        "statusCode": 200,
        "body": {
            "message": "Success",
            "document_ids": document_ids,
            "sec_code": sec_code,
            "saved_document_ids": saved_document_ids,
        },
    }
