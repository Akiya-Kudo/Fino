import type { Construct } from "constructs";
import {
	createResourceName,
	ResourceType,
	ServiceGroupName,
} from "../util/cdk/naming";

const edinetEventBusName = (scope: Construct) =>
	createResourceName({
		scope,
		resourceType: ResourceType.EVENT_BUS,
		serviceGroupName: ServiceGroupName.ECHO,
		baseResourceName: "edinet-event-bus",
	});

export const EchoEventContext = {
	edinet: {
		eventBus: {
			NAME: edinetEventBusName,
		},
		detailType: {
			EDINET_DOC_ID_REGISTER_TRIGGERED: "EdinetDocIDRegisterTriggered",
			EDINET_DOC_INGESTION_TRIGGERED: "EdinetDocIngestionTriggered",
		},
	},
	source: {
		CLI: "emitter.cli",
	},
	version: {
		V0: "0",
	},
};
