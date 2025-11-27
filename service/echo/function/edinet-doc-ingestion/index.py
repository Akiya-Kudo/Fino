import os
from typing import Optional
import tempfile
from pathlib import Path

import boto3
from boto3.dynamodb.conditions import Key
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.parser import event_parser
import schema as schemas
from edinet import EdinetClient
from pyiceberg.catalog import load_catalog
from pyiceberg.exceptions import NoSuchTableError
from pyiceberg.schema import Schema
from pyiceberg.types import StringType, NestedField
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
            try:
                _save_to_iceberg(sec_code, document_id, document_data)
            except Exception as iceberg_error:
                logger.error(f"Failed to save to Iceberg for document {document_id}: {iceberg_error}")
                # Iceberg保存失敗時は状態をREADYに戻してリトライ可能にする
                _update_ingestion_state(partition_key, document_id, "READY")
                raise
            
            # Update state to COMPLETED (DynamoDB更新失敗時のためにtry-except)
            try:
                _update_ingestion_state(partition_key, document_id, "COMPLETED")
            except Exception as db_error:
                logger.error(f"Failed to update state to COMPLETED for {document_id}: {db_error}")
                # データは保存済みなので、成功としてカウント（冪等性のため）
                logger.warning(f"Document {document_id} saved to Iceberg but state update failed")
            
            ingested_document_ids.append(document_id)
            logger.info(f"Successfully ingested document: {document_id}")
            
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {e}")
            # 状態をERRORに更新（既にREADYに戻されている場合もあるが、最終的な状態として記録）
            try:
                _update_ingestion_state(partition_key, document_id, "ERROR")
            except Exception as update_error:
                logger.error(f"Failed to update error state for {document_id}: {update_error}")
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
    tmp_file_path = None
    
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
        # 一時ファイルに書き込んでから読み込む（delete=Falseで明示的に制御）
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.zip', delete=False) as tmp_file:
            tmp_file.write(document_data)
            tmp_file_path = tmp_file.name
        
        try:
            # ZIPファイルからCSVを読み込み
            df = pd.read_csv(tmp_file_path, compression='zip', encoding='utf-8')
            
            # データが空の場合は処理をスキップ
            if df.empty:
                logger.warning(f"Document {document_id} contains no data, skipping")
                return
            
            # メタデータ列を追加
            df['document_id'] = document_id
            df['sec_code'] = sec_code
            
            # Icebergテーブルの取得または作成
            try:
                iceberg_table = catalog.load_table(full_table_name)
                logger.info(f"Loaded existing Iceberg table: {full_table_name}")
            except NoSuchTableError:
                logger.info(f"Table {full_table_name} does not exist, creating new table")
                iceberg_table = _create_iceberg_table(catalog, namespace, table_name, df)
            
            # Icebergテーブルに追記
            iceberg_table.append(df)
            
            logger.info(f"Successfully saved document {document_id} to Iceberg table {full_table_name}")
            
        except pd.errors.EmptyDataError:
            logger.warning(f"Document {document_id} is empty or invalid CSV format")
            raise
        except Exception as e:
            logger.error(f"Error processing CSV data for document {document_id}: {e}")
            raise
            
    except Exception as e:
        logger.error(f"Error saving to Iceberg: {e}")
        raise
    finally:
        # 一時ファイルの確実な削除
        if tmp_file_path and Path(tmp_file_path).exists():
            try:
                Path(tmp_file_path).unlink()
                logger.debug(f"Deleted temporary file: {tmp_file_path}")
            except Exception as cleanup_error:
                logger.warning(f"Failed to delete temporary file {tmp_file_path}: {cleanup_error}")


def _create_iceberg_table(catalog, namespace: str, table_name: str, sample_df: pd.DataFrame):
    """Create a new Iceberg table based on DataFrame schema"""
    try:
        # namespaceの作成（存在しない場合）
        try:
            catalog.create_namespace(namespace)
            logger.info(f"Created namespace: {namespace}")
        except Exception:
            # 既に存在する場合は無視
            logger.debug(f"Namespace {namespace} already exists")
        
        # DataFrameのスキーマからIcebergスキーマを生成
        # 基本的なスキーマ定義（実際のカラムは動的に追加）
        iceberg_fields = []
        field_id = 1
        
        for col_name, dtype in sample_df.dtypes.items():
            # Pandas dtypeをIceberg型にマッピング
            if dtype == 'object':
                iceberg_type = StringType()
            elif dtype == 'int64':
                from pyiceberg.types import LongType
                iceberg_type = LongType()
            elif dtype == 'float64':
                from pyiceberg.types import DoubleType
                iceberg_type = DoubleType()
            elif dtype == 'bool':
                from pyiceberg.types import BooleanType
                iceberg_type = BooleanType()
            else:
                # デフォルトは文字列型
                iceberg_type = StringType()
            
            iceberg_fields.append(
                NestedField(field_id=field_id, name=col_name, field_type=iceberg_type, required=False)
            )
            field_id += 1
        
        iceberg_schema = Schema(*iceberg_fields)
        
        # テーブル作成
        full_table_name = f"{namespace}.{table_name}"
        table = catalog.create_table(
            identifier=full_table_name,
            schema=iceberg_schema,
        )
        
        logger.info(f"Created new Iceberg table: {full_table_name}")
        return table
        
    except Exception as e:
        logger.error(f"Error creating Iceberg table {namespace}.{table_name}: {e}")
        raise
