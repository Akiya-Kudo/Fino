import type { Construct } from "constructs";

export type ContextKey = "projectName";

interface getContextArgs {
	scope: Construct;
	key: ContextKey;
}

export const getContext = ({ scope, key }: getContextArgs) => {
	return scope.node.tryGetContext(key);
};

/**
 * FIXME: 環境が増えた場合には撮り方を考える必要あり。環境変数として環境名を指定するようにする（lilomap）か、他にあるんかね
 */
export const getTargetEnv = () => {
	return process.env.CDK_DEFAULT_ACCOUNT === "000000000000" ? "Local" : "Prd";
};
