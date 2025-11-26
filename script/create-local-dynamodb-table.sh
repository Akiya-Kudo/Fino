#!/bin/bash

# DynamoDB Localにテーブルを作成するスクリプト

ENDPOINT_URL="http://localhost:8000"
TABLE_NAME="fino-local-ingestion-state-table"
REGION="ap-northeast-1"

echo "Creating DynamoDB table: ${TABLE_NAME}"

aws dynamodb create-table \
  --endpoint-url "${ENDPOINT_URL}" \
  --region "${REGION}" \
  --table-name "${TABLE_NAME}" \
  --attribute-definitions \
    AttributeName=data_source_group,AttributeType=S \
    AttributeName=document_id,AttributeType=S \
  --key-schema \
    AttributeName=data_source_group,KeyType=HASH \
    AttributeName=document_id,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST

echo "Table creation initiated. Waiting for table to be active..."

aws dynamodb wait table-exists \
  --endpoint-url "${ENDPOINT_URL}" \
  --region "${REGION}" \
  --table-name "${TABLE_NAME}"

echo "Table ${TABLE_NAME} is now active!"

