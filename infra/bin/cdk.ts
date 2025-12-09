#!/usr/bin/env node
import * as cdk from "aws-cdk-lib/core";
import { EchoEdinetIngestionStack } from "../lib/echo/edinet-ingestion-stack";
import { IngestionStateTableStack } from "../lib/echo/ingestion-state-table-stack";
import { HothLakeHouseStack } from "../lib/hoth/lakehouse-stack";

const app = new cdk.App();
const hothLakeHouseStack = new HothLakeHouseStack(app);

const ingestionStateStoreStack = new IngestionStateTableStack(app);

const echoEdinetIngestionStack = new EchoEdinetIngestionStack(app, {
	ingestionStateTable: ingestionStateStoreStack.ingestionStateTable,
	ingestionStateTableEndpoint: ingestionStateStoreStack.tableEndpoint,
});

echoEdinetIngestionStack.addDependency(hothLakeHouseStack);
