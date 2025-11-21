import { Duration, RemovalPolicy, type StackProps } from "aws-cdk-lib";
import * as s3 from "aws-cdk-lib/aws-s3";
import type { Construct } from "constructs";
import { type BaseInfo, BaseStack } from "../base/base-stack";
import {
	createResourceName,
	ResourceType,
	ServiceGroupName,
} from "../util/cdk/naming";
import { SystemGroup } from "../util/cdk/tagging";

export class HothRawStorageStack extends BaseStack {
	public readonly bucket: s3.Bucket;
	constructor(scope: Construct, props?: StackProps) {
		const baseInfo: BaseInfo = {
			serviceGroupName: ServiceGroupName.HOTH,
			serviceBaseName: "RawStorage",
			systemGroupName: SystemGroup.STORAGE,
		};
		super(scope, baseInfo, props);

		const bucketName = createResourceName({
			scope,
			baseResourceName: "raw-storage",
			resourceType: ResourceType.S3_BUCKET,
			serviceGroupName: ServiceGroupName.HOTH,
		});

		// TODO: Lifecycle の "Expiration" ルールを設定して削除ルールを設定して、不要なデータを自動で削除するようにする
		this.bucket = new s3.Bucket(this, "RawStorageBucket", {
			bucketName,
			blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
			removalPolicy: RemovalPolicy.RETAIN,
			// WORM（Write Once Read Many）のオブジェクトロックを設定するためにバージョニングが必須
			versioned: true,
			// ストーレージは明示的削除を必須化する（lockはバージョン単位で行われるため上書きはできてしまう）
			objectLockEnabled: true,
			// バッチ処理を考慮して1日でロックしておく
			objectLockDefaultRetention: s3.ObjectLockRetention.governance(
				Duration.days(1),
			),
			// 7日以上経過したデータは設計上しないため自動削除する
			lifecycleRules: [
				{
					expiration: Duration.days(7),
				},
			],
		});
	}
}
