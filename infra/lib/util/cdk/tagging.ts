import { type Stack, Tags } from "aws-cdk-lib";

export enum SystemGroup {
	API = "API",

	DISTRIBUTION = "Distribution",
	STORAGE = "Storage",
	JOB = "Job",
	AUTH = "Auth",
	COMMON = "Common",
	CICD = "CICD",
	SECURITY = "Security",
	MANAGE = "Manage", //(AWS Configなど)
	NONE = "none", // cdk import時にタグを追加しない用
}

export function addCommonTags(stack: Stack, systemGroup?: SystemGroup): void {
	const defaultSystemGroup = SystemGroup.NONE;

	const tags = Tags.of(stack);
	tags.add("Project", stack.node.tryGetContext("projectName"));
	tags.add(
		"Project-Env",
		stack.node.tryGetContext("projectName") +
			"-" +
			stack.node.tryGetContext("targetEnv"),
	);
	tags.add("SystemGroup", systemGroup ?? defaultSystemGroup);
	tags.add("Stack", stack.stackName);
}
