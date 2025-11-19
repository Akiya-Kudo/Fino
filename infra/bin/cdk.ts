#!/usr/bin/env node
import * as cdk from "aws-cdk-lib/core";
import { HothRawStorageStack } from "../lib/hoth/raw-storage";
import { getTargetEnv } from "../lib/util/cdk/context";

const app = new cdk.App();

const targetEnv = getTargetEnv();
console.log(targetEnv);
throw new Error(targetEnv.toString());

new HothRawStorageStack(app, {
	env: {},
});
