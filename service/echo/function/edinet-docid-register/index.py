import os
from typing import Any, Dict

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()

dynamodb = boto3.resource("dynamodb")


@logger.inject_lambda_context(log_event=True)
def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    # Edinet Document ID Register Lambda Function

    ## Description
    - eventから書類IDを取得し、DynamoDBのIngestion Stateに登録する
        - PK: edinet/<sec_code>
        - Sort Key: document_id
    """
    logger.info(f"Event: {event}")

    # テーブル名を環境変数から取得
    table_name = os.environ.get("INGESTION_STATE_TABLE_NAME")
    if not table_name:
        error_msg = "INGESTION_STATE_TABLE_NAME environment variable is not set"
        logger.error(error_msg)
        return {"statusCode": 500, "body": error_msg}

    table = dynamodb.Table(table_name)

    # イベントからdocument_idsを取得
    detail = event.get("detail", {})
    document_ids = detail.get("document_ids", [])
    sec_code = detail.get("sec_code")

    if not document_ids:
        error_msg = "document_ids not found in event detail"
        logger.error(error_msg)
        return {"statusCode": 400, "body": error_msg}

    if not sec_code:
        error_msg = "sec_code not found in event detail"
        logger.error(error_msg)
        return {"statusCode": 400, "body": error_msg}

    # 各document_idをDynamoDBに保存
    partition_key = f"edinet/{sec_code}"
    saved_count = 0
    errors = []

    for document_id in document_ids:
        try:
            table.put_item(
                Item={
                    "data_source_group": partition_key,
                    "sec_code": document_id,  # Sort Keyとしてdocument_idを保存
                }
            )
            saved_count += 1
            logger.info(f"Saved document_id: {document_id} with PK: {partition_key}")
        except Exception as e:
            error_msg = f"Failed to save document_id {document_id}: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)

    if errors:
        return {
            "statusCode": 207,  # Multi-Status
            "body": {
                "saved_count": saved_count,
                "total_count": len(document_ids),
                "errors": errors,
            },
        }

    logger.info(f"Successfully saved {saved_count} document_ids")
    return {
        "statusCode": 200,
        "body": {
            "message": "Success",
            "saved_count": saved_count,
            "total_count": len(document_ids),
        },
    }
