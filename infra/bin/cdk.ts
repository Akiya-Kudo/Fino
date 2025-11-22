#!/usr/bin/env node
import * as cdk from "aws-cdk-lib/core";
import { EchoRawStorageStack } from "../lib/echo/raw-storage";

const app = new cdk.App();

new EchoRawStorageStack(app, {
	env: {},
});
