import * as tables from "@aws-cdk/aws-s3tables-alpha";
import { RemovalPolicy, type StackProps } from "aws-cdk-lib";
import type { Construct } from "constructs";
import { type BaseInfo, BaseStack } from "../base/base-stack";
import {
	createResourceName,
	ResourceType,
	ServiceGroupName,
} from "../util/cdk/naming";
import { SystemGroup } from "../util/cdk/tagging";

export class HothLakeHouseStack extends BaseStack {
	constructor(scope: Construct, props?: StackProps) {
		const baseInfo: BaseInfo = {
			serviceGroupName: ServiceGroupName.HOTH,
			serviceBaseName: "LakeHouse",
			systemGroupName: SystemGroup.STORAGE,
		};
		super(scope, baseInfo, props);

		/**
		 * Resource Names
		 */
		const tableBucketName = createResourceName({
			scope,
			baseResourceName: "lakehouse-storage",
			resourceType: ResourceType.S3_TABLE_BUCKET,
			serviceGroupName: ServiceGroupName.HOTH,
		});
		const financialNamespaceName = createResourceName({
			scope,
			baseResourceName: "financial",
			resourceType: ResourceType.S3_TABLE_NAMESPACE,
			serviceGroupName: ServiceGroupName.HOTH,
		});
		const tableName = createResourceName({
			scope,
			baseResourceName: "lakehouse-table",
			resourceType: ResourceType.S3_TABLE,
			serviceGroupName: ServiceGroupName.HOTH,
		});

		/**
		 * Resources
		 */
		const tableBucket = new tables.TableBucket(this, "TableBucket", {
			tableBucketName: tableBucketName,
			removalPolicy: RemovalPolicy.RETAIN,
		});

		const financialNamespace = new tables.Namespace(this, "Namespace", {
			namespaceName: financialNamespaceName,
			tableBucket,
		});

		const table = new tables.Table(this, "Table", {
			namespace: financialNamespace,
			tableName: tableName,
			openTableFormat: tables.OpenTableFormat.ICEBERG,
			icebergMetadata: {
				icebergSchema: {
					schemaFieldList: [
						{
							name: "id",
							type: "int",
							required: true,
						},
						{
							name: "name",
							type: "string",
						},
					],
				},
			},
			/**
			 * 圧縮戦略の設定。既定では、テーブルのソート順に基づいて最適なコンパクション戦略が選択される。
			 * @see https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-maintenance.html#s3-tables-maintenance-compaction-strategies
			 */
			compaction: {
				status: tables.Status.ENABLED,
				targetFileSizeMb: 128, // 指定必須。
			},
			/**
			 * スナップショット管理の設定。デフォルトで有効。
			 * @see https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-maintenance.html#s3-tables-maintenance-snapshot-management
			 */
			snapshotManagement: {
				status: tables.Status.ENABLED,
				maxSnapshotAgeHours: 48, // スナップショットの最大保持期間。 デフォルトは 120 時間（5 日）
				minSnapshotsToKeep: 3, // 保持する最小スナップショット数。デフォルトは 1
			},
		});
	}
}
