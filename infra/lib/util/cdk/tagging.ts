import { type Stack, Tags } from "aws-cdk-lib";

export type SystemGroup =
	| "API"
	| "Distribution"
	| "Storage"
	| "Auth"
	| "Common"
	| "CICD"
	| "Security"
	| "Manage" //(AWS Configなど)
	| "none"; // cdk import時にタグを追加しない用

export function addCommonTags(stack: Stack, systemGroup?: SystemGroup): void {
	const defaultSystemGroup = "none";

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
