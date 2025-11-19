import type { StackProps } from "aws-cdk-lib";
import * as s3 from "aws-cdk-lib/aws-s3";
import type { Construct } from "constructs";
import { type BaseInfo, BaseStack } from "../base/base-stack";

export class HothRawStorageStack extends BaseStack {
	public readonly bucket: s3.Bucket;
	constructor(scope: Construct, props?: StackProps) {
		const baseInfo: BaseInfo = {
			serviceGroupName: "Hoth",
			serviceName: "RawStorage",
			systemGroupName: "Storage",
		};
		super(scope, baseInfo, props);

		this.bucket = new s3.Bucket(this, "RawStorageBucket", {});
	}
}
