import { Construct } from "constructs";
import { BaseInfo, BaseStack } from "../base/base-stack";
import { Duration, StackProps } from "aws-cdk-lib";
import { ServiceGroupName } from "../util/cdk/naming";
import { SystemGroup } from "../util/cdk/tagging";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as iam from "aws-cdk-lib/aws-iam";
import * as s3 from "aws-cdk-lib/aws-s3";
import * as path from "path";

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

    // Lambda実行ロールの作成
    const lambdaExecutionRole = new iam.Role(this, "LambdaExecutionRole", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName(
          "service-role/AWSLambdaBasicExecutionRole"
        ),
      ],
    });

    // S3読み取り権限を追加
    if (props?.dataStorageBucket) {
      props.dataStorageBucket.grantRead(lambdaExecutionRole);
    } else {
      // バケットが渡されない場合は、すべてのS3バケットへの読み取り権限を付与
      lambdaExecutionRole.addToPolicy(
        new iam.PolicyStatement({
          actions: ["s3:GetObject", "s3:ListBucket"],
          resources: ["*"],
        })
      );
    }

    // Glue Data Catalog読み取り権限を追加
    lambdaExecutionRole.addToPolicy(
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
      })
    );

    // Data Access Lambda関数
    this.dataAccessFunction = new lambda.Function(this, "DataAccessFunction", {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: "index.lambda_handler",
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../../lambda/echo/data-access")
      ),
      role: lambdaExecutionRole,
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
        path.join(__dirname, "../../lambda/echo/metadata")
      ),
      role: lambdaExecutionRole,
      timeout: Duration.seconds(30),
      memorySize: 256,
      environment: {
        GLUE_DATABASE_NAME: glueDatabaseName,
      },
    });

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
      this.dataAccessFunction,
      {
        proxy: true,
      }
    );

    dataTableResource.addMethod("GET", dataIntegration, {
      apiKeyRequired: true,
    });

    // /metadata リソースの作成
    const metadataResource = this.api.root.addResource("metadata");
    const metadataTablesResource = metadataResource.addResource("tables");
    const metadataTableResource = metadataTablesResource.addResource("{table_name}");

    const metadataIntegration = new apigateway.LambdaIntegration(
      this.metadataFunction,
      {
        proxy: true,
      }
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
