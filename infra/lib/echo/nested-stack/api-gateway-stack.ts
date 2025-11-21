import type { NestedStackProps } from "aws-cdk-lib";
import { NestedStack } from "aws-cdk-lib";
import * as apigatewayv2 from "aws-cdk-lib/aws-apigatewayv2";
import type * as lambda from "aws-cdk-lib/aws-lambda";
import type { Construct } from "constructs";
import {
	createResourceName,
	ResourceType,
	ServiceGroupName,
} from "../../util/cdk/naming";

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
	public readonly api: apigatewayv2.HttpApi;

	constructor(
		scope: Construct,
		id: string,
		props: EchoApiGatewayNestedStackProps,
	) {
		super(scope, id, props);

		const { dataAccessFunction, metadataFunction } = props;

		const apigatewayName = createResourceName({
			scope,
			baseResourceName: "echo-api",
			resourceType: ResourceType.HTTP_APIGATEWAY,
			serviceGroupName: ServiceGroupName.ECHO,
		});

		// API Gateway REST APIの作成
		this.api = new apigatewayv2.HttpApi(this, "EchoApi", {
			apiName: apigatewayName,
			description: "API for accessing financial data",
			disableExecuteApiEndpoint: false,
		});

		// API Keyの作成
		const apiKey = new apigatewayv2.ApiKey(this, "EchoApiKey", {
			apiKeyName: "FinoEchoApiKey",
			description: "API Key for Fino Echo Data API",
		});

		// Usage Planの作成
		const usagePlan = new apigatewayv2.UsagePlan(this, "EchoUsagePlan", {
			usagePlanName: resourceName,
			description: "Usage plan for Fino Echo Data API",
			throttle: {
				rateLimit: 100,
				burstLimit: 200,
			},
			quota: {
				limit: 10000,
				period: apigatewayv2.Period.DAY,
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
