import boto3

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    """
    # Edinet Document ID Register Lambda Function

    ## Description
    - eventから書類IDを取得し、DynamoDBのIngestion Stateに登録する
    """
    print(event)
    print(context)
    return {"statusCode": 200, "body": "Hello, World!"}
