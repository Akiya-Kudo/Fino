import { Duration, NestedStack, type NestedStackProps } from "aws-cdk-lib";
import * as iam from "aws-cdk-lib/aws-iam";
import * as lambda from "aws-cdk-lib/aws-lambda";
import type * as s3 from "aws-cdk-lib/aws-s3";
import type { Construct } from "constructs";
import * as path from "path";

export interface EchoLambdaNestedStackProps extends NestedStackProps {
	/**
	 * データストレージ用のS3バケット
	 */
	dataStorageBucket?: s3.IBucket;
	/**
	 * Glue Data Catalogのデータベース名
	 */
	glueDatabaseName: string;
}

export class EchoLambdaNestedStack extends NestedStack {
	public readonly dataAccessFunction: lambda.Function;
	public readonly metadataFunction: lambda.Function;
	public readonly lambdaExecutionRole: iam.Role;

	constructor(scope: Construct, id: string, props: EchoLambdaNestedStackProps) {
		super(scope, id, props);

		const { dataStorageBucket, glueDatabaseName } = props;

		// Lambda実行ロールの作成
		this.lambdaExecutionRole = new iam.Role(this, "LambdaExecutionRole", {
			assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
			managedPolicies: [
				iam.ManagedPolicy.fromAwsManagedPolicyName(
					"service-role/AWSLambdaBasicExecutionRole",
				),
			],
		});

		// S3読み取り権限を追加
		if (dataStorageBucket) {
			dataStorageBucket.grantRead(this.lambdaExecutionRole);
		} else {
			// バケットが渡されない場合は、すべてのS3バケットへの読み取り権限を付与
			this.lambdaExecutionRole.addToPolicy(
				new iam.PolicyStatement({
					actions: ["s3:GetObject", "s3:ListBucket"],
					resources: ["*"],
				}),
			);
		}

		// Glue Data Catalog読み取り権限を追加
		this.lambdaExecutionRole.addToPolicy(
			new iam.PolicyStatement({
				actions: [
					"glue:GetDatabase",
					"glue:GetTable",
					"glue:GetTables",
					"glue:GetPartition",
					"glue:GetPartitions",
				],
				resources: [
					`arn:aws:glue:${this.region}:${this.account}:catalog`,
					`arn:aws:glue:${this.region}:${this.account}:database/${glueDatabaseName}`,
					`arn:aws:glue:${this.region}:${this.account}:table/${glueDatabaseName}/*`,
				],
			}),
		);

		// Data Access Lambda関数
		this.dataAccessFunction = new lambda.Function(this, "DataAccessFunction", {
			runtime: lambda.Runtime.PYTHON_3_12,
			handler: "index.lambda_handler",
			code: lambda.Code.fromAsset(
				path.join(__dirname, "../../../../service/echo/lambda/data-access"),
			),
			role: this.lambdaExecutionRole,
			timeout: Duration.minutes(5),
			memorySize: 1024,
			environment: {
				GLUE_DATABASE_NAME: glueDatabaseName,
			},
		});

		// Metadata Lambda関数
		this.metadataFunction = new lambda.Function(this, "MetadataFunction", {
			runtime: lambda.Runtime.PYTHON_3_12,
			handler: "index.lambda_handler",
			code: lambda.Code.fromAsset(
				path.join(__dirname, "../../../../service/echo/lambda/metadata"),
			),
			role: this.lambdaExecutionRole,
			timeout: Duration.seconds(30),
			memorySize: 256,
			environment: {
				GLUE_DATABASE_NAME: glueDatabaseName,
			},
		});
	}
}
