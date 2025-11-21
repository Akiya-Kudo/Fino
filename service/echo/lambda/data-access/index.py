import json
import boto3
import pyarrow.parquet as pq
import pandas as pd
import io
import os
from typing import Any, Dict, List, Optional
from urllib.parse import unquote

s3_client = boto3.client('s3')
glue_client = boto3.client('glue')


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    S3 TablesからParquetファイルを取得し、JSON/CSV形式で返却する
    
    パスパラメータ:
        table_name: テーブル名
    
    クエリパラメータ:
        limit: 取得する行数の上限 (デフォルト: 1000, 最大: 10000)
        columns: カンマ区切りのカラム名リスト (省略時は全カラム)
        format: 出力形式 (json または csv, デフォルト: json)
        s3_path: 直接S3パスを指定する場合 (s3://bucket/key)
    """
    try:
        # パスパラメータとクエリパラメータを取得
        path_params = event.get('pathParameters', {}) or {}
        query_params = event.get('queryStringParameters', {}) or {}
        
        table_name = path_params.get('table_name', '')
        limit = int(query_params.get('limit', '1000'))
        columns = query_params.get('columns', '').split(',') if query_params.get('columns') else None
        output_format = query_params.get('format', 'json').lower()
        s3_path = query_params.get('s3_path', '')
        
        # リミット制限
        if limit > 10000:
            limit = 10000
        
        # S3パスの決定
        if s3_path:
            # 直接S3パス指定の場合
            s3_path = unquote(s3_path)
            if not s3_path.startswith('s3://'):
                return error_response(400, 's3_path must start with s3://')
            
            bucket, key = parse_s3_path(s3_path)
        elif table_name:
            # テーブル名からGlue Data Catalogを参照してS3パスを取得
            try:
                database_name = os.environ.get('GLUE_DATABASE_NAME', 'fino_database')
                table_info = glue_client.get_table(
                    DatabaseName=database_name,
                    Name=table_name
                )
                location = table_info['Table']['StorageDescriptor']['Location']
                bucket, key = parse_s3_path(location)
            except glue_client.exceptions.EntityNotFoundException:
                return error_response(404, f'Table {table_name} not found in Glue Catalog')
            except Exception as e:
                return error_response(500, f'Error accessing Glue Catalog: {str(e)}')
        else:
            return error_response(400, 'Either table_name or s3_path must be provided')
        
        # S3からParquetファイルを読み取り
        try:
            # S3オブジェクトを取得
            response = s3_client.get_object(Bucket=bucket, Key=key)
            parquet_buffer = io.BytesIO(response['Body'].read())
            
            # Parquetファイルを読み込み
            table = pq.read_table(parquet_buffer, columns=columns)
            df = table.to_pandas()
            
            # 行数制限を適用
            if len(df) > limit:
                df = df.head(limit)
            
            # 出力形式に応じて変換
            if output_format == 'csv':
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'text/csv',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key',
                        'Access-Control-Allow-Methods': 'GET,OPTIONS'
                    },
                    'body': csv_buffer.getvalue()
                }
            else:
                # JSON形式 (デフォルト)
                data = df.to_dict(orient='records')
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key',
                        'Access-Control-Allow-Methods': 'GET,OPTIONS'
                    },
                    'body': json.dumps({
                        'table_name': table_name,
                        'rows': len(data),
                        'columns': list(df.columns),
                        'data': data
                    }, default=str)
                }
        
        except s3_client.exceptions.NoSuchKey:
            return error_response(404, f'File not found: s3://{bucket}/{key}')
        except Exception as e:
            return error_response(500, f'Error reading parquet file: {str(e)}')
    
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}')


def parse_s3_path(s3_path: str) -> tuple:
    """S3パス (s3://bucket/key) をbucketとkeyに分割"""
    path = s3_path.replace('s3://', '')
    parts = path.split('/', 1)
    if len(parts) != 2:
        raise ValueError(f'Invalid S3 path: {s3_path}')
    return parts[0], parts[1]


def error_response(status_code: int, message: str) -> Dict[str, Any]:
    """エラーレスポンスを生成"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        },
        'body': json.dumps({
            'error': message
        })
    }

