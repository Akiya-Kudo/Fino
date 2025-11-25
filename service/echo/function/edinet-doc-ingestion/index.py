import json
import boto3

dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    """
    # Edinet Document Ingestion Lambda Function

    ## Description
        - DynamoDBのIngestion Stateを参照し、未取得の書類を取得する
        - EDINET APIを叩いて書類を取得する
        - Hoth Data LakeHouseに書き込みを行う(PyIceberg)
    """
    print(f"Received event: {json.dumps(event)}")
    
    # EventBridgeから来る場合、detailフィールドを取得
    detail = event.get("detail", event)
    
    # detailが文字列の場合はJSONパース
    if isinstance(detail, str):
        try:
            detail = json.loads(detail)
        except json.JSONDecodeError as e:
            print(f"Failed to parse detail as JSON: {e}")
            return {"statusCode": 400, "body": "Invalid JSON in detail field"}
    
    # document_idsを取得
    document_ids = detail.get("document_ids", []) if isinstance(detail, dict) else []
    
    print(f"Processing document_ids: {document_ids}")
    
    # TODO: 実際の処理を実装
    
    return {"statusCode": 200, "body": "Hello, World!"}
