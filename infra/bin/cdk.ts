#!/usr/bin/env node
import * as cdk from "aws-cdk-lib/core";
import { HothRawStorageStack } from "../lib/hoth/raw-storage-stack";
import { EchoApiStack } from "../lib/echo/api-stack";

const app = new cdk.App();

// データストレージスタックの作成
const hothStorageStack = new HothRawStorageStack(app, {
	env: {},
});

// データアクセスAPIスタックの作成
new EchoApiStack(app, {
	env: {},
	dataStorageBucket: hothStorageStack.bucket,
	glueDatabaseName: "fino_database",
});
