#!/usr/bin/env node
import * as cdk from "aws-cdk-lib/core";
import { HothLakeHouseStack } from "../lib/hoth/lakehouse-stack";

const app = new cdk.App();

new HothLakeHouseStack(app);
