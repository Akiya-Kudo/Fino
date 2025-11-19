import * as cdk from "aws-cdk-lib";
import type { Construct } from "constructs";
import { createStackName } from "../util/cdk/naming";
import { addCommonTags, type SystemGroup } from "../util/cdk/tagging";

export interface BaseInfo {
	/** サービスグループ名 */
	serviceGroupName: string;
	/** システムグループ名 */
	systemGroupName?: SystemGroup;
	/** サービス名 */
	serviceName: string;
}

export class BaseStack extends cdk.Stack {
	constructor(scope: Construct, baseInfo: BaseInfo, props?: cdk.StackProps) {
		const { serviceGroupName, systemGroupName, serviceName } = baseInfo;
		const stackName = createStackName({
			scope,
			serviceGroupName,
			serviceName,
		});
		super(scope, stackName, props);
		addCommonTags(this, systemGroupName);
	}
}
