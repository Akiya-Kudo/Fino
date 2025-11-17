import * as cdk from "aws-cdk-lib";
import type { Construct } from "constructs";
import { createStackName } from "../util/cdk/naming";
import { addCommonTags, type SystemGroup } from "../util/cdk/tagging";

export interface BaseInfo {
	baseName: string;
	systemGroup?: SystemGroup;
}

export class BaseStack extends cdk.Stack {
	constructor(scope: Construct, baseInfo: BaseInfo, props?: cdk.StackProps) {
		const { baseName, systemGroup } = baseInfo;
		const stackName = createStackName({ scope, baseName });
		super(scope, stackName, props);
		addCommonTags(this, systemGroup);
	}
}
