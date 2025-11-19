# Fino

### アーキテクチャ概要

- AWS Cloud にホスト
- サーバーレス・マネージドサービスを活用して、コスト削減
- 初期段階は、イベント駆動により、常時稼働を行わない構成
- Iceberg テーブルスキーマにより、拡張しやすい形のデータ・レイクハウスを構築
- 様々な形式のデータを取り込めるように、中継ストレージを S3 で導入

<img src="./docs/assets/architecture.jpg" width="1000px" />

### コンポーネント・サービス群

---

##### Hoth（Data LakeHouse）

- S3 Table

  - データレイクハウス用ストレージ

- S3

  - 生データ用ストレージ

- Glue Job

  - 生データから　 Perquet 形式へ整形用　 ETL
  - モデリング・集計用 ETL

- Lambda

  - 外部データリソースからのデータ収集の実装（Edinet からの request + html 解析等の処理）

- DynamoSB

  - データ整形処理を、軽量に行うためのバッチ管理用テーブル
  - 生データの変換状況を管理する

---

##### Echo（Backned API）

- API Gateway

  - API Endpoint

- Lambda

  - Data カタログからデータをクエリする
  - ETL の実行イベントの発火

- Athena
  - マネージドサービスのクエリサービス
  - API とは別に導入し、データ分析で自由にデータにアクセスできるようにする
  - ※ データの更新・テーブルスキーマの変更は、基本行わないように権限管理

---

##### Naboo（Portfolio Service）

- API Gateway

  - API Endpoint

- Lambda

  - リクエスト処理

- DynamoDB
  - ユーザ管理
  - 取引データ管理

---

##### Bespin（Bashboard）

- Grafana

  - データの可視化をするローカル・ダッシュボード
  - ポートフォリオサービスと・データ基盤両方にアクセスできるようにクライアント部分を切り分けて管理
  - IaC：Grafana SDK によりプロビジョンできるようにする

---

##### Coruscant（Jupyter Nootebook）

- Jupyter Nootbook

  - Athenea SDK でスキーマ上のデータ クエリ対応
  - DuckDB でスキーマを経由せずに軽量クエリ分析
  - diskcache ライブラリで、ローカルディスクのキャッシュ機構を作成して、クエリコストを削減

---

##### N1（Emitter CLI Tool）

- Golang ? Python ? CLI
  - 定型的なデータ基盤へのイベント実行を CLI から実行できるようにする
  - Playwirght を使用して、ポートフォリオ・サービスと連携し、ポートフォリオ情報を管理できるようにする
