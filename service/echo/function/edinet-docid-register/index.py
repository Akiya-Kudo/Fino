from typing import Any, Dict

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import EventBridgeEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()

dynamodb = boto3.resource("dynamodb")


@logger.inject_lambda_context(log_event=True)
def handler(event: EventBridgeEvent, context: LambdaContext) -> Dict[str, Any]:
    """
    # Edinet Document ID Register Lambda Function

    ## Description
    - eventから書類IDを取得し、DynamoDBのIngestion Stateに登録する
    """
    logger.info(f"Event: {event}")
    return {"statusCode": 200, "body": "Hello, World!"}
