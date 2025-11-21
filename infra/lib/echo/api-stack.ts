import type { StackProps } from "aws-cdk-lib";
import type * as apigateway from "aws-cdk-lib/aws-apigateway";
import type * as lambda from "aws-cdk-lib/aws-lambda";
import type * as s3 from "aws-cdk-lib/aws-s3";
import type { Construct } from "constructs";
import { type BaseInfo, BaseStack } from "../base/base-stack";
import { ServiceGroupName } from "../util/cdk/naming";
import { SystemGroup } from "../util/cdk/tagging";
import { EchoApiGatewayNestedStack } from "./nested-stack/api-gateway-stack";
import { EchoLambdaNestedStack } from "./nested-stack/lambda-stack";

interface EchoApiStackProps extends StackProps {
	/**
	 * データストレージ用のS3バケット
	 * HothRawStorageStackから渡される
	 */
	dataStorageBucket?: s3.IBucket;
	/**
	 * Glue Data Catalogのデータベース名
	 */
	glueDatabaseName?: string;
}

export class EchoApiStack extends BaseStack {
	public readonly api: apigateway.RestApi;
	public readonly dataAccessFunction: lambda.Function;
	public readonly metadataFunction: lambda.Function;

	constructor(scope: Construct, props?: EchoApiStackProps) {
		const baseInfo: BaseInfo = {
			serviceGroupName: ServiceGroupName.ECHO,
			systemGroupName: SystemGroup.API,
			serviceBaseName: "Api",
		};
		super(scope, baseInfo, props);

		const glueDatabaseName = props?.glueDatabaseName || "fino_database";

		// Lambda Nested Stack
		const lambdaStack = new EchoLambdaNestedStack(this, "LambdaStack", {
			dataStorageBucket: props?.dataStorageBucket,
			glueDatabaseName,
		});

		// API Gateway Nested Stack
		const apiGatewayStack = new EchoApiGatewayNestedStack(
			this,
			"ApiGatewayStack",
			{
				dataAccessFunction: lambdaStack.dataAccessFunction,
				metadataFunction: lambdaStack.metadataFunction,
			},
		);

		// 外部からアクセス可能なプロパティを設定
		this.api = apiGatewayStack.api;
		this.dataAccessFunction = lambdaStack.dataAccessFunction;
		this.metadataFunction = lambdaStack.metadataFunction;
	}
}
