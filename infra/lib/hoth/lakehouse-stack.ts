import * as tables from "@aws-cdk/aws-s3tables-alpha";
import { RemovalPolicy, type StackProps } from "aws-cdk-lib";
import type { Construct } from "constructs";
import {
	type BaseInfo,
	BaseStack,
	type BaseStackProps,
} from "../base/base-stack";
import {
	createResourceName,
	ResourceType,
	ServiceGroupName,
} from "../util/cdk/naming";
import { SystemGroup } from "../util/cdk/tagging";

/**
 * # Hoth Stack（Data LakeHouse）
 * Data LakeHouse の基盤スタック
 *
 * ### ☑️ IaCで管理すべきもの：
 * - Raw 層の Iceberg Tables（Echo Stack（Ingestion Pipeline）やデータリソースからの書き込み用途のテーブル）
 *   → Ingestion Pipeline と密結合しているため、Schema と Partition を固定すべき
 *   → データ契約（Data Contract）としてインフラの一部として扱う
 *
 * ### 🆖 IaC で管理しないもの：
 * - Refined 層の Iceberg Tables（分析用途のテーブル）
 * - Mart 層（BI 用テーブル）
 *   → モデリングの進化が頻繁なため、SQL / ETL で管理
 * - ad-hoc テーブル
 *   → BI チームが自由に新テーブルを作れるようにして、schema evolution やsnapshot management の恩恵を活かす
 */
export class HothLakeHouseStack extends BaseStack {
	/**
	 * 	### Data Lake House Table Bucket
	 * テーブル定義を管理するためのバケット
	 */
	public readonly tableBucket: tables.TableBucket;
	/**
	 * ### Raw 層の Namespace
	 * Ingestion Pipeline が書き込む Raw テーブル用の名前空間
	 */
	public readonly rawNamespace: tables.Namespace;
	/**
	 * ### Financial 層の Namespace
	 * Refined / Mart 層のテーブル用の名前空間（CDK ではNamespaceのみ定義）
	 */
	public readonly financialNamespace: tables.Namespace;
	/**
	 * ### Raw 層のテーブル
	 * Ingestion Pipeline が書き込む Raw テーブル
	 */
	public readonly rawTable: tables.Table;

	constructor(scope: Construct, props?: BaseStackProps) {
		const baseInfo: BaseInfo = {
			serviceGroupName: ServiceGroupName.HOTH,
			serviceBaseName: "LakeHouse",
			systemGroupName: SystemGroup.STORAGE,
		};
		super(scope, baseInfo, props);

		// ===== Custom Local Resource =====
		if (props?.isRequiredCustomLocalResource) {
			console.log("Custom Local Resource is required");
			return;
		}

		// ===== Table Bucket =====

		const tableBucketName = createResourceName({
			scope,
			baseResourceName: "lakehouse-storage",
			resourceType: ResourceType.S3_TABLE_BUCKET,
			serviceGroupName: ServiceGroupName.HOTH,
		});

		this.tableBucket = new tables.TableBucket(this, "TableBucket", {
			tableBucketName,
			removalPolicy: RemovalPolicy.RETAIN,
		});

		// ===== Namespace =====

		const rawNamespaceName = createResourceName({
			scope,
			baseResourceName: "raw",
			resourceType: ResourceType.S3_TABLE_NAMESPACE,
			serviceGroupName: ServiceGroupName.HOTH,
		});
		const financialNamespaceName = createResourceName({
			scope,
			baseResourceName: "financial",
			resourceType: ResourceType.S3_TABLE_NAMESPACE,
			serviceGroupName: ServiceGroupName.HOTH,
		});

		this.rawNamespace = new tables.Namespace(this, "RawNamespace", {
			namespaceName: rawNamespaceName,
			tableBucket: this.tableBucket,
		});

		this.financialNamespace = new tables.Namespace(this, "FinancialNamespace", {
			namespaceName: financialNamespaceName,
			tableBucket: this.tableBucket,
		});

		// ===== Raw Table =====

		const rawTableName = createResourceName({
			scope,
			baseResourceName: "raw",
			resourceType: ResourceType.S3_TABLE,
			serviceGroupName: ServiceGroupName.HOTH,
		});

		this.rawTable = new tables.Table(this, "RawTable", {
			namespace: this.rawNamespace,
			tableName: rawTableName,
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
							name: "timestamp",
							type: "timestamp",
							required: true,
						},
						{
							name: "data",
							type: "string",
						},
					],
				},
			},
			compaction: {
				status: tables.Status.ENABLED,
				targetFileSizeMb: 128,
			},
			snapshotManagement: {
				status: tables.Status.ENABLED,
				maxSnapshotAgeHours: 48,
				minSnapshotsToKeep: 3,
			},
		});
	}
}
