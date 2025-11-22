import * as cdk from "aws-cdk-lib/core";
import * as s3 from "aws-cdk-lib/aws-s3";
import { BaseInfo, BaseStack } from "../base/base-stack";
import { Construct } from 'constructs';

interface HothProps extends cdk.StackProps {
  // lakehouseのデータレイヤー設定
  enableRawLayer?: boolean;
  enableProcessedLayer?: boolean;
  enableCuratedLayer?: boolean;
  
  // ライフサイクルポリシー設定（日数）
  lifecycleConfig?: {
    transitionToInfrequentAccessDays?: number;
    transitionToGlacierDays?: number;
    transitionToDeepArchiveDays?: number;
    noncurrentVersionTransitionToGlacierDays?: number;
    noncurrentVersionExpirationDays?: number;
    expiredObjectDeleteMarkerDays?: number;
  };
}

/**
 * Hoth - Lakehouse用のS3データストレージスタック
 * 
 * 以下のレイヤーを提供：
 * - Raw Layer: 生データの保存
 * - Processed Layer: 変換・クレンジング後のデータ
 * - Curated Layer: 分析可能な形式のデータ
 * 
 * 各レイヤーでバージョニングとライフサイクルポリシーを適用し、
 * コスト最適化とデータガバナンスを実現
 */
export class Hoth extends BaseStack {
  public readonly rawBucket?: s3.Bucket;
  public readonly processedBucket?: s3.Bucket;
  public readonly curatedBucket?: s3.Bucket;
  public readonly logBucket: s3.Bucket;

  constructor(scope: Construct, baseName: string, props?: HothProps) {
    const baseInfo: BaseInfo = {
      baseName,
      systemGroup: "Storage",
    };
    super(scope, baseInfo, props);

    // デフォルト設定
    const config = {
      enableRawLayer: props?.enableRawLayer ?? true,
      enableProcessedLayer: props?.enableProcessedLayer ?? true,
      enableCuratedLayer: props?.enableCuratedLayer ?? true,
      lifecycleConfig: {
        transitionToInfrequentAccessDays: props?.lifecycleConfig?.transitionToInfrequentAccessDays ?? 30,
        transitionToGlacierDays: props?.lifecycleConfig?.transitionToGlacierDays ?? 90,
        transitionToDeepArchiveDays: props?.lifecycleConfig?.transitionToDeepArchiveDays ?? 180,
        noncurrentVersionTransitionToGlacierDays: props?.lifecycleConfig?.noncurrentVersionTransitionToGlacierDays ?? 30,
        noncurrentVersionExpirationDays: props?.lifecycleConfig?.noncurrentVersionExpirationDays ?? 90,
        expiredObjectDeleteMarkerDays: props?.lifecycleConfig?.expiredObjectDeleteMarkerDays ?? 1,
      },
    };

    // アクセスログ用バケット
    this.logBucket = this.createLogBucket();

    // Raw Layer: 生データ保存用（最も長期保存）
    if (config.enableRawLayer) {
      this.rawBucket = this.createDataBucket(
        'raw',
        'Raw data layer for lakehouse',
        {
          transitionToInfrequentAccessDays: config.lifecycleConfig.transitionToInfrequentAccessDays,
          transitionToGlacierDays: config.lifecycleConfig.transitionToGlacierDays,
          transitionToDeepArchiveDays: config.lifecycleConfig.transitionToDeepArchiveDays,
          noncurrentVersionTransitionToGlacierDays: config.lifecycleConfig.noncurrentVersionTransitionToGlacierDays,
          noncurrentVersionExpirationDays: config.lifecycleConfig.noncurrentVersionExpirationDays,
        }
      );

      new cdk.CfnOutput(this, 'RawBucketName', {
        value: this.rawBucket.bucketName,
        description: 'Raw data layer bucket name',
        exportName: `${this.stackName}-RawBucket`,
      });
    }

    // Processed Layer: 処理済みデータ（中期保存）
    if (config.enableProcessedLayer) {
      this.processedBucket = this.createDataBucket(
        'processed',
        'Processed data layer for lakehouse',
        {
          transitionToInfrequentAccessDays: Math.floor(config.lifecycleConfig.transitionToInfrequentAccessDays / 2),
          transitionToGlacierDays: Math.floor(config.lifecycleConfig.transitionToGlacierDays * 0.7),
          transitionToDeepArchiveDays: config.lifecycleConfig.transitionToDeepArchiveDays,
          noncurrentVersionTransitionToGlacierDays: Math.floor(config.lifecycleConfig.noncurrentVersionTransitionToGlacierDays / 2),
          noncurrentVersionExpirationDays: Math.floor(config.lifecycleConfig.noncurrentVersionExpirationDays * 0.7),
        }
      );

      new cdk.CfnOutput(this, 'ProcessedBucketName', {
        value: this.processedBucket.bucketName,
        description: 'Processed data layer bucket name',
        exportName: `${this.stackName}-ProcessedBucket`,
      });
    }

    // Curated Layer: 分析用データ（短期保存）
    if (config.enableCuratedLayer) {
      this.curatedBucket = this.createDataBucket(
        'curated',
        'Curated data layer for lakehouse',
        {
          transitionToInfrequentAccessDays: Math.floor(config.lifecycleConfig.transitionToInfrequentAccessDays / 3),
          transitionToGlacierDays: Math.floor(config.lifecycleConfig.transitionToGlacierDays / 2),
          transitionToDeepArchiveDays: config.lifecycleConfig.transitionToGlacierDays, // より早くアーカイブ
          noncurrentVersionTransitionToGlacierDays: 7,
          noncurrentVersionExpirationDays: Math.floor(config.lifecycleConfig.noncurrentVersionExpirationDays / 2),
        }
      );

      new cdk.CfnOutput(this, 'CuratedBucketName', {
        value: this.curatedBucket.bucketName,
        description: 'Curated data layer bucket name',
        exportName: `${this.stackName}-CuratedBucket`,
      });
    }

    new cdk.CfnOutput(this, 'LogBucketName', {
      value: this.logBucket.bucketName,
      description: 'Access logs bucket name',
      exportName: `${this.stackName}-LogBucket`,
    });
  }

  /**
   * アクセスログ保存用バケットの作成
   */
  private createLogBucket(): s3.Bucket {
    const bucket = new s3.Bucket(this, 'LogBucket', {
      bucketName: `${this.stackName.toLowerCase()}-logs`,
      // ログバケットは暗号化必須
      encryption: s3.BucketEncryption.S3_MANAGED,
      // ログバケット自体にはバージョニング不要
      versioned: false,
      // パブリックアクセスブロック
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      // 削除保護
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      autoDeleteObjects: false,
      // ライフサイクルポリシー: ログは一定期間後に削除
      lifecycleRules: [
        {
          id: 'DeleteOldLogs',
          enabled: true,
          expiration: cdk.Duration.days(90), // 90日後にログ削除
          transitions: [
            {
              storageClass: s3.StorageClass.INFREQUENT_ACCESS,
              transitionAfter: cdk.Duration.days(30),
            },
          ],
        },
      ],
    });

    return bucket;
  }

  /**
   * データレイヤー用バケットの作成
   */
  private createDataBucket(
    layerName: string,
    description: string,
    lifecycleConfig: {
      transitionToInfrequentAccessDays: number;
      transitionToGlacierDays: number;
      transitionToDeepArchiveDays: number;
      noncurrentVersionTransitionToGlacierDays: number;
      noncurrentVersionExpirationDays: number;
    }
  ): s3.Bucket {
    const bucket = new s3.Bucket(this, `${this.capitalizeFirst(layerName)}Bucket`, {
      bucketName: `${this.stackName.toLowerCase()}-${layerName}`,
      // バージョニング有効化
      versioned: true,
      // 暗号化: S3管理キー（必要に応じてKMSに変更可能）
      encryption: s3.BucketEncryption.S3_MANAGED,
      // パブリックアクセスブロック
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      // 削除保護: 本番環境ではRETAINを推奨
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      autoDeleteObjects: false,
      // アクセスログの有効化
      serverAccessLogsBucket: this.logBucket,
      serverAccessLogsPrefix: `${layerName}/`,
      // ライフサイクルポリシー
      lifecycleRules: [
        {
          id: `${layerName}-CurrentVersionLifecycle`,
          enabled: true,
          transitions: [
            {
              storageClass: s3.StorageClass.INFREQUENT_ACCESS,
              transitionAfter: cdk.Duration.days(lifecycleConfig.transitionToInfrequentAccessDays),
            },
            {
              storageClass: s3.StorageClass.GLACIER,
              transitionAfter: cdk.Duration.days(lifecycleConfig.transitionToGlacierDays),
            },
            {
              storageClass: s3.StorageClass.DEEP_ARCHIVE,
              transitionAfter: cdk.Duration.days(lifecycleConfig.transitionToDeepArchiveDays),
            },
          ],
        },
        {
          id: `${layerName}-NoncurrentVersionLifecycle`,
          enabled: true,
          noncurrentVersionTransitions: [
            {
              storageClass: s3.StorageClass.GLACIER,
              transitionAfter: cdk.Duration.days(lifecycleConfig.noncurrentVersionTransitionToGlacierDays),
            },
          ],
          noncurrentVersionExpiration: cdk.Duration.days(lifecycleConfig.noncurrentVersionExpirationDays),
        },
        {
          id: `${layerName}-ExpiredObjectDeleteMarker`,
          enabled: true,
          expiredObjectDeleteMarker: true,
        },
      ],
      // CORS設定（必要に応じて調整）
      cors: [
        {
          allowedMethods: [
            s3.HttpMethods.GET,
            s3.HttpMethods.PUT,
            s3.HttpMethods.POST,
            s3.HttpMethods.DELETE,
            s3.HttpMethods.HEAD,
          ],
          allowedOrigins: ['*'], // 本番環境では制限を推奨
          allowedHeaders: ['*'],
          maxAge: 3000,
        },
      ],
    });

    // バケットにタグを追加
    cdk.Tags.of(bucket).add('Layer', layerName);
    cdk.Tags.of(bucket).add('Description', description);

    return bucket;
  }

  /**
   * 文字列の最初の文字を大文字にする
   */
  private capitalizeFirst(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
}
