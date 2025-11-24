import boto3

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    """
    # Edinet Document Ingestion Lambda Function

    ## Description
        - DynamoDBのIngestion Stateを参照し、未取得の書類を取得する
        - EDINET APIを叩いて書類を取得する
        - Hoth Data LakeHouseに書き込みを行う（PyIceberg）
    """
    print(event)
    print(context)
    return {"statusCode": 200, "body": "Hello, World!"}
