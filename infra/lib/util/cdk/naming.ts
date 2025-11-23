import type { Construct } from "constructs";
import { getContext, getTargetEnv } from "./context";

/**
 * Stack Name
 */

export enum ServiceGroupName {
	HOTH = "Hoth",
	ECHO = "Echo",
}

/**
 * Resource Type
 */
export enum ResourceType {
	S3_BUCKET = "S3Bucket",
	S3_TABLE = "S3Table",
	S3_TABLE_BUCKET = "S3TableBucket",
	S3_TABLE_NAMESPACE = "S3TableNamespace",
	DYNAMODB = "DynamoDB",
}
interface createStackNameArgs {
	scope: Construct;
	serviceGroupName: string;
	serviceBaseName: string;
}

interface createResourceNameArgs {
	scope: Construct;
	resourceType?: ResourceType;
	baseResourceName: string;
	serviceGroupName?: ServiceGroupName;
}

export const connect = (arr: string[], sep = "-"): string => {
	return arr.filter((str) => !!str).join(sep);
};

export const createStackName = ({
	scope,
	serviceGroupName,
	serviceBaseName,
}: createStackNameArgs) => {
	const projectName = getContext({ scope, key: "projectName" });
	const envName = getTargetEnv();

	return connect([projectName, envName, serviceGroupName, serviceBaseName]);
};

/**
 * Resource Name
 */

export const createResourceName = ({
	scope,
	resourceType,
	baseResourceName,
	serviceGroupName,
}: createResourceNameArgs) => {
	const projectName = getContext({ scope, key: "projectName" });
	const envName = getTargetEnv();

	switch (resourceType) {
		case ResourceType.S3_BUCKET:
		case ResourceType.S3_TABLE_BUCKET:
			if (!serviceGroupName)
				throw new Error(
					"S3バケットのリソース名を作成する場合はserviceGroupNameが必須です",
				);
			return connect([
				projectName.toLowerCase(),
				envName.toLowerCase(),
				serviceGroupName.toLowerCase(),
				baseResourceName.toLowerCase(),
			]);
		case ResourceType.S3_TABLE:
		case ResourceType.S3_TABLE_NAMESPACE:
			return connect([baseResourceName.toLowerCase()]);
		default:
			return connect([projectName, envName, baseResourceName]);
	}
};

/**
 * SSM Parameter Name
 */

export type ssmParameterAcmArnName = "sub_certificate_arn";

export const makeSsmParameterName = ({
	scope,
	baseName,
}: {
	scope: Construct;
	baseName: ssmParameterAcmArnName;
}) => {
	const projectName = connect(
		["/", getContext({ scope, key: "projectName" }).toLowerCase()],
		"",
	);
	const envName = getTargetEnv().toLowerCase();

	return connect([projectName, envName, baseName], "/");
};
