import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import type { Construct } from "constructs";
import {
	type BaseInfo,
	BaseStack,
	type BaseStackProps,
} from "../base/base-stack";
import { getEnvRemovalPolicy } from "../util/cdk/context";
import {
	createResourceName,
	ResourceType,
	ServiceGroupName,
} from "../util/cdk/naming";
import { SystemGroup } from "../util/cdk/tagging";

/**
 * # Ingestion State Store Stack
 * Ingestion State を管理するための DynamoDB テーブルを作成するスタック
 */
export class IngestionStateStoreStack extends BaseStack {
	/**
	 * ## Ingestion State Table
	 *
	 * ### Partition Key : data_source_group のハッシュ値をパーティションキーとすることで、Ingestion Pipelineでの一括取得が可能になる
	 * - data_source_group: データソースグループ名
	 *   - EDINET: data_source_name#sec_code: データソース名#証券コード
	 *
	 * ### Sort Key : document_identifier
	 * - document_identifier: ドキュメント識別子
	 *   - EDINET: docID: 書類管理番号
	 */
	public readonly ingestionStateTable: dynamodb.Table;

	constructor(scope: Construct, props?: BaseStackProps) {
		const baseInfo: BaseInfo = {
			serviceGroupName: ServiceGroupName.ECHO,
			systemGroupName: SystemGroup.STORAGE,
			serviceBaseName: "IngestionStateStore",
		};
		super(scope, baseInfo, props);

		// DynamoDB Table

		const ingestionStateTableName = createResourceName({
			scope,
			serviceGroupName: ServiceGroupName.ECHO,
			resourceType: ResourceType.DYNAMODB,
			baseResourceName: "ingestion-state-table",
		});

		this.ingestionStateTable = new dynamodb.Table(this, "IngestionStateTable", {
			tableName: ingestionStateTableName,
			partitionKey: {
				name: "data_source_group",
				type: dynamodb.AttributeType.STRING,
			},
			sortKey: {
				name: "sec_code",
				type: dynamodb.AttributeType.STRING,
			},
			billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
			// max Unitを念の為設定しておく
			maxReadRequestUnits: 20,
			maxWriteRequestUnits: 20,
			pointInTimeRecoverySpecification: {
				pointInTimeRecoveryEnabled: true,
				recoveryPeriodInDays: 7, // 7 daysまでなら、遡れるようにする
			},
			removalPolicy: getEnvRemovalPolicy(),
		});
	}
}
