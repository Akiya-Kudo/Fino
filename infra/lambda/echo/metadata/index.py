import json
import boto3
import os
from typing import Any, Dict, List, Optional

glue_client = boto3.client('glue')


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Glue Data Catalogからメタデータを取得
    
    パス:
        GET /metadata/tables - 全テーブル一覧を取得
        GET /metadata/tables/{table_name} - 特定テーブルの詳細情報を取得
    
    クエリパラメータ:
        database: データベース名 (省略時は環境変数から取得)
    """
    try:
        # パスパラメータとクエリパラメータを取得
        path_params = event.get('pathParameters', {}) or {}
        query_params = event.get('queryStringParameters', {}) or {}
        
        table_name = path_params.get('table_name', '')
        database_name = query_params.get('database', os.environ.get('GLUE_DATABASE_NAME', 'fino_database'))
        
        if table_name:
            # 特定テーブルの詳細情報を取得
            return get_table_details(database_name, table_name)
        else:
            # 全テーブル一覧を取得
            return list_tables(database_name)
    
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}')


def list_tables(database_name: str) -> Dict[str, Any]:
    """データベース内の全テーブル一覧を取得"""
    try:
        # データベース情報を取得
        try:
            database = glue_client.get_database(Name=database_name)
            database_info = {
                'name': database['Database']['Name'],
                'description': database['Database'].get('Description', ''),
                'location': database['Database'].get('LocationUri', '')
            }
        except glue_client.exceptions.EntityNotFoundException:
            return error_response(404, f'Database {database_name} not found')
        
        # テーブル一覧を取得
        tables = []
        next_token = None
        
        while True:
            if next_token:
                response = glue_client.get_tables(
                    DatabaseName=database_name,
                    NextToken=next_token
                )
            else:
                response = glue_client.get_tables(DatabaseName=database_name)
            
            for table in response.get('TableList', []):
                tables.append({
                    'name': table['Name'],
                    'description': table.get('Description', ''),
                    'location': table.get('StorageDescriptor', {}).get('Location', ''),
                    'table_type': table.get('TableType', ''),
                    'columns': len(table.get('StorageDescriptor', {}).get('Columns', [])),
                    'partitions': len(table.get('PartitionKeys', [])),
                    'created_at': table.get('CreateTime', '').isoformat() if table.get('CreateTime') else '',
                    'updated_at': table.get('UpdateTime', '').isoformat() if table.get('UpdateTime') else ''
                })
            
            next_token = response.get('NextToken')
            if not next_token:
                break
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps({
                'database': database_info,
                'tables': tables,
                'count': len(tables)
            }, default=str)
        }
    
    except Exception as e:
        return error_response(500, f'Error listing tables: {str(e)}')


def get_table_details(database_name: str, table_name: str) -> Dict[str, Any]:
    """特定テーブルの詳細情報を取得"""
    try:
        response = glue_client.get_table(
            DatabaseName=database_name,
            Name=table_name
        )
        
        table = response['Table']
        storage_descriptor = table.get('StorageDescriptor', {})
        
        # カラム情報を整形
        columns = []
        for col in storage_descriptor.get('Columns', []):
            columns.append({
                'name': col['Name'],
                'type': col['Type'],
                'comment': col.get('Comment', '')
            })
        
        # パーティションキー情報を整形
        partition_keys = []
        for pk in table.get('PartitionKeys', []):
            partition_keys.append({
                'name': pk['Name'],
                'type': pk['Type'],
                'comment': pk.get('Comment', '')
            })
        
        # テーブルパラメータ (Icebergメタデータ等)
        parameters = table.get('Parameters', {})
        
        table_details = {
            'name': table['Name'],
            'database': database_name,
            'description': table.get('Description', ''),
            'table_type': table.get('TableType', ''),
            'location': storage_descriptor.get('Location', ''),
            'input_format': storage_descriptor.get('InputFormat', ''),
            'output_format': storage_descriptor.get('OutputFormat', ''),
            'serde_info': {
                'serialization_library': storage_descriptor.get('SerdeInfo', {}).get('SerializationLibrary', ''),
                'parameters': storage_descriptor.get('SerdeInfo', {}).get('Parameters', {})
            },
            'columns': columns,
            'partition_keys': partition_keys,
            'parameters': parameters,
            'created_at': table.get('CreateTime', '').isoformat() if table.get('CreateTime') else '',
            'updated_at': table.get('UpdateTime', '').isoformat() if table.get('UpdateTime') else '',
            'is_iceberg': parameters.get('table_type') == 'ICEBERG'
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps(table_details, default=str)
        }
    
    except glue_client.exceptions.EntityNotFoundException:
        return error_response(404, f'Table {table_name} not found in database {database_name}')
    except Exception as e:
        return error_response(500, f'Error getting table details: {str(e)}')


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

