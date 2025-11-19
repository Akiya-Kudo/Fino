#!/usr/bin/env node
import * as cdk from "aws-cdk-lib/core";
import { FinoStack } from "../lib/fino-stack";
import { HothRawStorageStack } from "../lib/hoth/raw-storage";

const app = new cdk.App();
new FinoStack(app, "FinoStack", {
	env: {},
});

new HothRawStorageStack(app, {
	env: {},
});
