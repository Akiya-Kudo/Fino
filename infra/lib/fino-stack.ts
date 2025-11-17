import type * as cdk from "aws-cdk-lib/core";
import type { Construct } from "constructs";
import { type BaseInfo, BaseStack } from "./base/base-stack";

// import * as sqs from 'aws-cdk-lib/aws-sqs';

interface FinoStackProps extends cdk.StackProps {}

export class FinoStack extends BaseStack {
	constructor(scope: Construct, baseName: string, props?: FinoStackProps) {
		const baseInfo: BaseInfo = {
			baseName,
			systemGroup: "none",
		};
		super(scope, baseInfo, props);
	}
}
