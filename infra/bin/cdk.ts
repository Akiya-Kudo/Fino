#!/usr/bin/env node
import * as cdk from "aws-cdk-lib/core";
import { EchoEdinetIngestionStack } from "../lib/echo/edinet-ingestion-stack";
import { HothLakeHouseStack } from "../lib/hoth/lakehouse-stack";

const app = new cdk.App();

const hothLakeHouseStack = new HothLakeHouseStack(app);

const echoEdinetIngestionStack = new EchoEdinetIngestionStack(app);

echoEdinetIngestionStack.addDependency(hothLakeHouseStack);
