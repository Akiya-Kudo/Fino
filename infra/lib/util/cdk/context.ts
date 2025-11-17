import type { Construct } from "constructs";

export type ContextKey = "projectName" | "targetEnv";

interface getContextArgs {
	scope: Construct;
	key: ContextKey;
}

export const getContext = ({ scope, key }: getContextArgs) => {
	return scope.node.tryGetContext(key);
};
