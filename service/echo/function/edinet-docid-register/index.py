import json
import os
from typing import Any, Dict

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.validation.exceptions import SchemaValidationError
from aws_lambda_powertools.utilities.validation import validator
import schema as schemas

# ENVIRONMENT VARIABLES
table_endpoint = os.environ.get("INGESTION_STATE_TABLE_ENDPOINT")
table_name = os.environ.get("INGESTION_STATE_TABLE_NAME")

# INITIALIZATION
dynamodb = boto3.resource("dynamodb", endpoint_url=table_endpoint)
table = dynamodb.Table(table_name)

logger = Logger()

# @logger.inject_lambda_context(log_event=True)
@validator(inbound_schema=schemas.INPUT, outbound_schema=schemas.OUTPUT)
def handler(event: schemas.INPUT, context: LambdaContext) -> schemas.OUTPUT:
    """
    # Edinet Document ID Register Lambda Function

    ## Description
    - eventから書類IDを取得し、DynamoDBのIngestion Stateに登録する
        - PK: edinet/<sec_code>
        - Sort Key: document_id
    - すでにレコードが存在する場合は、更新を加えない
    """
    print(json.dump(context))
    print(json.dump(context))
    print(json.dump(context))

    # イベントからdetailを取得
    detail = event.get("detail", event)
    
    # detailが文字列の場合はJSONパース
    if isinstance(detail, str):
        detail = json.loads(detail)

    # document_idsとsec_codeを取得
    document_ids = detail.get("document_ids", [])
    sec_code = detail.get("sec_code")

    if not document_ids:
        raise ValueError("document_ids not found in event detail")
    
    if not sec_code:
        raise ValueError("sec_code not found in event detail")

    # logger.info(f"document_ids: {document_ids}")
   

    # 各document_idをDynamoDBに保存
    partition_key = f"edinet/{sec_code}"

    for document_id in document_ids:
        table.put_item(
            Item={
                "data_source_group": partition_key,
                "document_id": document_id,  # Sort Keyとしてdocument_idを保存
                "ingestion_state": "READY",
            }
        )
        # logger.info(f"Saved document_id: {document_id}")

    # logger.info(f"Successfully saved {len(document_ids)} document_ids")
    
    return {
        "statusCode": 200,
        "body": {
            "message": "Success",
            "sec_code": sec_code,
            "saved_count": len(document_ids),
        },
    }
