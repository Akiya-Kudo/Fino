import type { NestedStackProps } from "aws-cdk-lib";
import { NestedStack } from "aws-cdk-lib";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import type * as lambda from "aws-cdk-lib/aws-lambda";
import type { Construct } from "constructs";

export interface EchoApiGatewayNestedStackProps extends NestedStackProps {
	/**
	 * Data Access Lambda関数
	 */
	dataAccessFunction: lambda.IFunction;
	/**
	 * Metadata Lambda関数
	 */
	metadataFunction: lambda.IFunction;
}

export class EchoApiGatewayNestedStack extends NestedStack {
	public readonly api: apigateway.RestApi;

	constructor(
		scope: Construct,
		id: string,
		props: EchoApiGatewayNestedStackProps,
	) {
		super(scope, id, props);

		const { dataAccessFunction, metadataFunction } = props;

		// API Gateway REST APIの作成
		this.api = new apigateway.RestApi(this, "EchoApi", {
			restApiName: "Fino Echo Data API",
			description: "API for accessing financial data from S3 Tables (Iceberg)",
			defaultCorsPreflightOptions: {
				allowOrigins: apigateway.Cors.ALL_ORIGINS,
				allowMethods: apigateway.Cors.ALL_METHODS,
				allowHeaders: [
					"Content-Type",
					"X-Amz-Date",
					"Authorization",
					"X-Api-Key",
					"X-Amz-Security-Token",
				],
			},
			apiKeySourceType: apigateway.ApiKeySourceType.HEADER,
		});

		// API Keyの作成
		const apiKey = this.api.addApiKey("EchoApiKey", {
			apiKeyName: "FinoEchoApiKey",
			description: "API Key for Fino Echo Data API",
		});

		// Usage Planの作成
		const usagePlan = this.api.addUsagePlan("EchoUsagePlan", {
			name: "FinoEchoUsagePlan",
			description: "Usage plan for Fino Echo Data API",
			throttle: {
				rateLimit: 100,
				burstLimit: 200,
			},
			quota: {
				limit: 10000,
				period: apigateway.Period.DAY,
			},
		});

		usagePlan.addApiKey(apiKey);

		// /data リソースの作成
		const dataResource = this.api.root.addResource("data");
		const dataTableResource = dataResource.addResource("{table_name}");

		// /data/{table_name} GET メソッド
		const dataIntegration = new apigateway.LambdaIntegration(
			dataAccessFunction,
			{
				proxy: true,
			},
		);

		dataTableResource.addMethod("GET", dataIntegration, {
			apiKeyRequired: true,
		});

		// /metadata リソースの作成
		const metadataResource = this.api.root.addResource("metadata");
		const metadataTablesResource = metadataResource.addResource("tables");
		const metadataTableResource =
			metadataTablesResource.addResource("{table_name}");

		const metadataIntegration = new apigateway.LambdaIntegration(
			metadataFunction,
			{
				proxy: true,
			},
		);

		// /metadata/tables GET メソッド (全テーブル一覧)
		metadataTablesResource.addMethod("GET", metadataIntegration, {
			apiKeyRequired: true,
		});

		// /metadata/tables/{table_name} GET メソッド (特定テーブルの詳細)
		metadataTableResource.addMethod("GET", metadataIntegration, {
			apiKeyRequired: true,
		});

		// Usage PlanにAPIステージを追加
		usagePlan.addApiStage({
			stage: this.api.deploymentStage,
		});
	}
}
