import type { Construct } from "constructs";
import {
	type BaseInfo,
	BaseStack,
	type BaseStackProps,
} from "../base/base-stack";
import { ServiceGroupName } from "../util/cdk/naming";
import { SystemGroup } from "../util/cdk/tagging";

export class EchoEdinetIngestionStack extends BaseStack {
	constructor(scope: Construct, props?: BaseStackProps) {
		const baseInfo: BaseInfo = {
			serviceGroupName: ServiceGroupName.ECHO,
			serviceBaseName: "EdinetIngestion",
			systemGroupName: SystemGroup.JOB,
		};
		super(scope, baseInfo, props);

		// Step Function
	}
}
