import * as pythonLambda from "@aws-cdk/aws-lambda-python-alpha";
import { Duration } from "aws-cdk-lib";
import type * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as events from "aws-cdk-lib/aws-events";
import * as targets from "aws-cdk-lib/aws-events-targets";
import * as iam from "aws-cdk-lib/aws-iam";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as stepfunctions from "aws-cdk-lib/aws-stepfunctions";
import * as tasks from "aws-cdk-lib/aws-stepfunctions-tasks";
import type { Construct } from "constructs";
import {
	type BaseInfo,
	BaseStack,
	type BaseStackProps,
} from "../base/base-stack";
import { getLambdaEntryPath } from "../util/cdk/context";
import {
	createResourceName,
	ResourceType,
	ServiceGroupName,
} from "../util/cdk/naming";
import { SystemGroup } from "../util/cdk/tagging";
import { EchoEventContext } from "./context";

interface EchoEdinetIngestionStackProps extends BaseStackProps {
	ingestionStateTable: dynamodb.Table;
}

/**
 * # Edinet Ingestion Workflow Stack
 * Edinet Ingestion Workflowを管理するためのスタック
 */
export class EchoEdinetIngestionStack extends BaseStack {
	/**
	 * ## Lambda (Edinet Document Ingestion)
	 */
	public readonly edinetDocIngestionLambda: pythonLambda.PythonFunction;

	/**
	 * ## Lambda (Edinet Document ID Register)
	 */
	public readonly edinetDocIdRegisterLambda: pythonLambda.PythonFunction;

	/**
	 * ## Step Function (Edinet Ingestion)
	 */
	public readonly stateMachine: stepfunctions.StateMachine;

	/**
	 * ## Event Rule for (Edinet Ingestion)
	 */
	public readonly eventRule: events.Rule;

	constructor(scope: Construct, props: EchoEdinetIngestionStackProps) {
		const baseInfo: BaseInfo = {
			serviceGroupName: ServiceGroupName.ECHO,
			systemGroupName: SystemGroup.JOB,
			serviceBaseName: "EdinetIngestion",
		};
		super(scope, baseInfo, props);

		// Lambda（Python）

		const edinetDocIdRegisterLambdaEntryPath = getLambdaEntryPath({
			serviceGroupName: "echo",
			functionName: "edinet-docid-register",
		});

		const edinetDocIdRegisterLambdaName = createResourceName({
			scope,
			resourceType: ResourceType.LAMBDA,
			serviceGroupName: ServiceGroupName.ECHO,
			baseResourceName: "edinet-docid-register",
		});

		this.edinetDocIdRegisterLambda = new pythonLambda.PythonFunction(
			this,
			"EdinetDocIdRegisterLambda",
			{
				functionName: edinetDocIdRegisterLambdaName,
				entry: edinetDocIdRegisterLambdaEntryPath,
				handler: "handler",
				runtime: lambda.Runtime.PYTHON_3_13,
				environment: {
					INGESTION_STATE_TABLE_NAME: props.ingestionStateTable.tableName,
				},
				bundling: {
					assetExcludes: [".venv", "__pycache__", "*.pyc"],
				},
			},
		);

		const edinetDocIngestionLambdaEntryPath = getLambdaEntryPath({
			serviceGroupName: "echo",
			functionName: "edinet-doc-ingestion",
		});

		const edinetDocIngestionLambdaName = createResourceName({
			scope,
			resourceType: ResourceType.LAMBDA,
			serviceGroupName: ServiceGroupName.ECHO,
			baseResourceName: "edinet-doc-ingestion",
		});

		this.edinetDocIngestionLambda = new pythonLambda.PythonFunction(
			this,
			"EdinetDocIngestionLambda",
			{
				functionName: edinetDocIngestionLambdaName,
				entry: edinetDocIngestionLambdaEntryPath,
				handler: "handler",
				runtime: lambda.Runtime.PYTHON_3_13,
				environment: {
					INGESTION_STATE_TABLE_NAME: props.ingestionStateTable.tableName,
				},
				bundling: {
					assetExcludes: [".venv", "__pycache__", "*.pyc"],
				},
			},
		);

		// Lambda Policy Role

		this.edinetDocIdRegisterLambda.addToRolePolicy(
			new iam.PolicyStatement({
				actions: ["dynamodb:PutItem", "dynamodb:GetItem"],
				resources: [props.ingestionStateTable.tableArn],
			}),
		);

		this.edinetDocIngestionLambda.addToRolePolicy(
			new iam.PolicyStatement({
				actions: ["dynamodb:PutItem", "dynamodb:GetItem"],
				resources: [props.ingestionStateTable.tableArn],
			}),
		);

		// Step Function Tasks

		// 別のパスで使用するため、新しいタスクインスタンスを作成
		const edinetDocIdRegisterTask = new tasks.LambdaInvoke(
			this,
			"EdinetDocIdRegisterTask",
			{
				lambdaFunction: this.edinetDocIdRegisterLambda,
				integrationPattern: stepfunctions.IntegrationPattern.REQUEST_RESPONSE,
			},
		);

		const edinetDocIdRegisterForIngestionTask = new tasks.LambdaInvoke(
			this,
			"EdinetDocIdRegisterForIngestionTask",
			{
				lambdaFunction: this.edinetDocIdRegisterLambda,
				integrationPattern: stepfunctions.IntegrationPattern.REQUEST_RESPONSE,
			},
		);

		const edinetDocIngestionTask = new tasks.LambdaInvoke(
			this,
			"EdinetDocIngestionTask",
			{
				lambdaFunction: this.edinetDocIngestionLambda,
				integrationPattern: stepfunctions.IntegrationPattern.REQUEST_RESPONSE,
			},
		);

		const waitTask = new stepfunctions.Wait(this, "Wait30sTask", {
			time: stepfunctions.WaitTime.duration(Duration.seconds(30)),
		});

		const successState = new stepfunctions.Succeed(this, "Success");

		// Step Function Workflow

		// EventBridgeのdetailを共通変数として抽出
		const extractDetailState = stepfunctions.Pass.jsonata(
			this,
			"ExtractDetail",
			{
				outputs: {
					detail: "$.detail",
					detailType: "$.detailType",
				},
			},
		);

		const docIngestionIterator = stepfunctions.Map.jsonata(
			this,
			"MapIterator",
			{
				maxConcurrency: 1,
				items: stepfunctions.ProvideItems.jsonata("{% $document_ids %}"),
			},
		).itemProcessor(edinetDocIngestionTask.next(waitTask));

		const docIngestionFlow = stepfunctions.Chain.start(
			edinetDocIdRegisterForIngestionTask,
		).next(docIngestionIterator);

		const workflow = stepfunctions.Chain.start(extractDetailState).next(
			stepfunctions.Choice.jsonata(this, "Choice")
				.when(
					stepfunctions.Condition.jsonata(
						`{% $states.input.detailType = '${EchoEventContext.edinet.detailType.EDINT_DOC_ID_REGISTER_TRIGGERED}' %}`,
					),
					edinetDocIdRegisterTask.next(successState),
				)
				.when(
					stepfunctions.Condition.jsonata(
						`{% $states.input.detailType = '${EchoEventContext.edinet.detailType.EDINT_DOC_INGESTION_TRIGGERED}' %}`,
					),
					docIngestionFlow.next(successState),
				)
				.otherwise(
					stepfunctions.Fail.jsonata(this, "UnsupportedEventType", {
						error: "UnsupportedEventType",
						cause: "Event type not supported",
					}),
				),
		);

		// Step Function
		const stateMachineName = createResourceName({
			scope,
			resourceType: ResourceType.STEP_FUNCTION,
			baseResourceName: "EdinetStateMachine",
		});

		this.stateMachine = new stepfunctions.StateMachine(this, "StateMachine", {
			stateMachineName,

			definition: workflow,
		});

		// Event Bridge

		const customEventBusName = createResourceName({
			scope,
			resourceType: ResourceType.EVENT_BUS,
			serviceGroupName: ServiceGroupName.ECHO,
			baseResourceName: "edinet-event-bus",
		});

		const customEventBus = new events.EventBus(this, "EventBus", {
			eventBusName: customEventBusName,
			description: "EventBus for Fino Edinet Ingestion",
		});

		const eventRuleName = createResourceName({
			scope,
			resourceType: ResourceType.EVNENT_RULE,
			baseResourceName: "EdinetIngestionEventRule",
		});

		this.eventRule = new events.Rule(this, "EventRule", {
			ruleName: eventRuleName,
			description: "Rule for Edinet Ingestion",
			eventBus: customEventBus,
			eventPattern: {
				version: [EchoEventContext.version.V0],
				source: [EchoEventContext.source.CLI],
				detailType: [
					EchoEventContext.edinet.detailType.EDINT_DOC_ID_REGISTER_TRIGGERED,
					EchoEventContext.edinet.detailType.EDINT_DOC_INGESTION_TRIGGERED,
				],
			},
			targets: [new targets.SfnStateMachine(this.stateMachine)],
		});
	}
}
