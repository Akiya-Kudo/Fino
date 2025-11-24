import * as cdk from "aws-cdk-lib";
import type { Construct } from "constructs";
import type { ServiceGroupName } from "./naming";

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

/**
 * set removal policy based on target environment
 */
export const getEnvRemovalPolicy = () => {
	return getTargetEnv() === "Prd"
		? cdk.RemovalPolicy.RETAIN
		: cdk.RemovalPolicy.DESTROY;
};

/**
 * サービスレイヤーの関数エントリーポイントのパスを生成する
 * @param serviceGroupName - サービスグループ名（例: ServiceGroupName.ECHO）
 * @param functionName - 関数名（例: "edinet-doc-ingestion"）
 * @param entryFile - エントリーファイル名（デフォルト: "main.py"）
 * @returns 関数エントリーポイントへの相対パス
 */
interface getLambdaEntryPathArgs {
	serviceGroupName: Lowercase<ServiceGroupName>;
	functionName: string;
	entryFile?: string;
}

export const getLambdaEntryPath = ({
	serviceGroupName,
	functionName,
}: getLambdaEntryPathArgs) => {
	const serviceGroupPath = serviceGroupName;
	return `../../service/${serviceGroupPath}/function/${functionName}/`;
};
