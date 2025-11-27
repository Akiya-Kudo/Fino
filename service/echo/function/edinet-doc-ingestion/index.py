import os
from typing import Optional
import tempfile

import boto3
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.parser import event_parser
import schema as schemas
from edinet import EdinetClient
from pyiceberg.catalog import load_catalog
import pandas as pd

# ENVIRONMENT VARIABLES
table_endpoint = os.environ.get("INGESTION_STATE_TABLE_ENDPOINT")
table_name = os.environ.get("INGESTION_STATE_TABLE_NAME")
s3_warehouse_path = os.environ.get("S3_WAREHOUSE_PATH", "s3://fino-lakehouse/warehouse")
iceberg_catalog_name = os.environ.get("ICEBERG_CATALOG_NAME", "default")

# INITIALIZATION
dynamodb = boto3.resource("dynamodb", endpoint_url=table_endpoint)
table = dynamodb.Table(table_name)

logger = Logger()


@logger.inject_lambda_context(log_event=True)
@event_parser(model=schemas.InputEvent)
def handler(event: schemas.InputEvent, context: LambdaContext) -> schemas.OutputEvent:
    """
    # Edinet Document Ingestion Lambda Function

    ## Description
        - DynamoDBのIngestion Stateを参照し、未取得の書類を取得する
        - EDINET APIを叩いて書類を取得する
        - Hoth Data LakeHouseに書き込みを行う(PyIceberg)
    """

    # Event Extract
    detail = event.detail
    document_ids = detail.document_ids
    sec_code = detail.sec_code

    # Generate Partition Key
    partition_key = f"edinet/{sec_code}"

    # Get READY documents from DynamoDB
    ready_document_ids = []
    for document_id in document_ids:
        try:
            response = table.get_item(
                Key={
                    "data_source_group": partition_key,
                    "document_id": document_id
                }
            )
            
            item = response.get("Item")
            if item and item.get("ingestion_state") == "READY":
                ready_document_ids.append(document_id)
                logger.info(f"Document {document_id} is READY for ingestion")
            else:
                logger.info(f"Document {document_id} is not READY (state: {item.get('ingestion_state') if item else 'NOT_FOUND'})")
        except Exception as e:
            logger.error(f"Error getting document {document_id} from DynamoDB: {e}")
            continue

    if not ready_document_ids:
        logger.info("No READY documents to process")
        return {
            "statusCode": 200,
            "body": {
                "message": "No READY documents to process",
                "document_ids": document_ids,
                "sec_code": sec_code,
                "ingested_count": 0,
            },
        }

    # Initialize Edinet Client
    edinet_client = EdinetClient()

    # Process each document
    ingested_document_ids = []
    for document_id in ready_document_ids:
        try:
            logger.info(f"Processing document: {document_id}")
            
            # Update state to PROCESSING
            _update_ingestion_state(partition_key, document_id, "PROCESSING")
            
            # Fetch document from EDINET API
            document_data = _fetch_edinet_document(edinet_client, document_id)
            
            if document_data is None:
                logger.error(f"Failed to fetch document {document_id}")
                _update_ingestion_state(partition_key, document_id, "ERROR")
                continue
            
            # Save to Iceberg table
            _save_to_iceberg(sec_code, document_id, document_data)
            
            # Update state to COMPLETED
            _update_ingestion_state(partition_key, document_id, "COMPLETED")
            
            ingested_document_ids.append(document_id)
            logger.info(f"Successfully ingested document: {document_id}")
            
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {e}")
            _update_ingestion_state(partition_key, document_id, "ERROR")
            continue

    logger.info(f"INGESTED COUNT: {len(ingested_document_ids)}")
    return {
        "statusCode": 200,
        "body": {
            "message": "Success",
            "document_ids": ingested_document_ids,
            "sec_code": sec_code,
            "ingested_count": len(ingested_document_ids),
        },
    }


def _update_ingestion_state(partition_key: str, document_id: str, state: str) -> None:
    """Update ingestion state in DynamoDB"""
    try:
        table.update_item(
            Key={
                "data_source_group": partition_key,
                "document_id": document_id
            },
            UpdateExpression="SET ingestion_state = :state",
            ExpressionAttributeValues={
                ":state": state
            }
        )
        logger.info(f"Updated state for {document_id} to {state}")
    except Exception as e:
        logger.error(f"Failed to update state for {document_id}: {e}")
        raise


def _fetch_edinet_document(client: EdinetClient, document_id: str) -> Optional[bytes]:
    """Fetch document from EDINET API"""
    try:
        # EDINET APIでドキュメントを取得（CSV形式）
        # type=2 でCSV形式を取得
        response = client.get_document(document_id, doc_type=2)
        
        if response:
            logger.info(f"Successfully fetched document {document_id}")
            return response
        else:
            logger.error(f"Empty response for document {document_id}")
            return None
            
    except Exception as e:
        logger.error(f"Error fetching document {document_id} from EDINET: {e}")
        return None


def _save_to_iceberg(sec_code: str, document_id: str, document_data: bytes) -> None:
    """Save document data to Iceberg table"""
    try:
        # Iceberg catalogの初期化
        catalog = load_catalog(
            iceberg_catalog_name,
            **{
                "type": "glue",
                "warehouse": s3_warehouse_path,
            }
        )
        
        # テーブル名の生成
        namespace = "edinet_raw"
        table_name = f"sec_code_{sec_code}"
        full_table_name = f"{namespace}.{table_name}"
        
        # データをDataFrameに変換
        # 一時ファイルに書き込んでから読み込む
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.zip', delete=False) as tmp_file:
            tmp_file.write(document_data)
            tmp_file_path = tmp_file.name
        
        try:
            # ZIPファイルからCSVを読み込み
            df = pd.read_csv(tmp_file_path, compression='zip', encoding='utf-8')
            
            # メタデータ列を追加
            df['document_id'] = document_id
            df['sec_code'] = sec_code
            
            # Icebergテーブルに追記
            iceberg_table = catalog.load_table(full_table_name)
            iceberg_table.append(df)
            
            logger.info(f"Successfully saved document {document_id} to Iceberg table {full_table_name}")
            
        finally:
            # 一時ファイルの削除
            import os as os_module
            if os_module.path.exists(tmp_file_path):
                os_module.remove(tmp_file_path)
            
    except Exception as e:
        logger.error(f"Error saving to Iceberg: {e}")
        raise
