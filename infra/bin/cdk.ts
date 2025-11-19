#!/usr/bin/env node
import * as cdk from "aws-cdk-lib/core";
import { HothRawStorageStack } from "../lib/hoth/raw-storage";

const app = new cdk.App();

new HothRawStorageStack(app, {
	env: {},
});
