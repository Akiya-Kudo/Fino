import type { Construct } from "constructs";
import { getContext } from "./context";

interface createStackNameArgs {
	scope: Construct;
	baseName: string;
}

export const connect = (arr: string[], sep = "-"): string => {
	return arr.filter((str) => !!str).join(sep);
};

export const createStackName = ({ scope, baseName }: createStackNameArgs) => {
	const projectName = getContext({ scope, key: "projectName" });
	const envName = getContext({ scope, key: "targetEnv" });

	return connect([projectName, envName, baseName]);
};

export type ssmParameterAcmArnName = "sub_certificate_arn";

interface createResourceNameArgs {
	scope: Construct;
	baseResourceName: string;
}

export const createResourceName = ({
	scope,
	baseResourceName,
}: createResourceNameArgs) => {
	const projectName = getContext({ scope, key: "projectName" });
	const envName = getContext({ scope, key: "targetEnv" });

	return connect([projectName, envName, baseResourceName]);
};

export const makeBucketName = ({
	scope,
	baseName,
}: {
	scope: Construct;
	baseName: string;
}) => {
	const projectName = getContext({ scope, key: "projectName" }).toLowerCase();
	const envName = getContext({ scope, key: "targetEnv" }).toLowerCase();

	return connect([projectName, envName, baseName.toLowerCase()]);
};

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
	const envName = getContext({ scope, key: "targetEnv" }).toLowerCase();

	return connect([projectName, envName, baseName], "/");
};
