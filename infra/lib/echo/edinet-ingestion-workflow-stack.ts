import * as events from "aws-cdk-lib/aws-events";
import * as targets from "aws-cdk-lib/aws-events-targets";
import * as stepfunctions from "aws-cdk-lib/aws-stepfunctions";
import type { Construct } from "constructs";
import {
	type BaseInfo,
	BaseStack,
	type BaseStackProps,
} from "../base/base-stack";
import {
	createResourceName,
	ResourceType,
	ServiceGroupName,
} from "../util/cdk/naming";
import { SystemGroup } from "../util/cdk/tagging";

/**
 * # Edinet Ingestion Workflow Stack
 * Edinet Ingestion Workflowを管理するためのスタック
 */
export class EchoEdinetIngestionStack extends BaseStack {
	/**
	 * ## Step Function (Edinet Ingestion)
	 */
	public readonly stateMachine: stepfunctions.StateMachine;

	/**
	 * ## Event Rule for (Edinet Ingestion)
	 */
	public readonly eventRule: events.Rule;

	constructor(scope: Construct, props?: BaseStackProps) {
		const baseInfo: BaseInfo = {
			serviceGroupName: ServiceGroupName.ECHO,
			systemGroupName: SystemGroup.JOB,
			serviceBaseName: "EdinetIngestion",
		};
		super(scope, baseInfo, props);

		// Lambda（Python）

		// Step Function

		const choiceState = new stepfunctions.Choice(this, "ChoiceState", {
			comment: "Choice state for Edinet Ingestion",
		});

		console.log("choiceState", choiceState);

		const stateMachineName = createResourceName({
			scope,
			resourceType: ResourceType.STEP_FUNCTION,
			baseResourceName: "EdinetStateMachine",
		});

		this.stateMachine = new stepfunctions.StateMachine(this, "StateMachine", {
			stateMachineName,

			definition: new stepfunctions.Pass(this, "Pass", {
				result: stepfunctions.Result.fromString("Hello, World!"),
			}),
		});

		// Event Bridge

		const customEventBusName = createResourceName({
			scope,
			resourceType: ResourceType.EVENT_BUS,
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
				version: ["0"],
				source: ["emitter.cli"],
				detailType: [
					"EdintDocIDRegisterTriggered",
					"EdintDocIngestionTriggered",
				],
			},
			targets: [new targets.SfnStateMachine(this.stateMachine)],
		});
	}
}
