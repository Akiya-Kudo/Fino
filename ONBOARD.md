# Fino Setup

### はじめに

[setup スクリプト](./script/setup.sh) を用意してるので下記をプロジェクトルートで実行してください

```sh
source ./script/setup.sh
```

### 使い方

上記の setup スクリプトを実行することでプロジェクトの実行に使用するコマンドを fino コマンドに集約されます。実態は makefile になるので、詳しくは[プロジェクトの Makefile](./Makefile)を参照してください。

#### 使えるコマンドの概要

##### cdk

- AWS リソースのインフラのデプロイ時に使用します

```
// 例
fino cdk deploy Sample-Stack
```

##### local

- Localstack を使用して AWS のエミュレーション環境を Local で実行でき m す。
- ローカルで動かしたい時や、動作確認でしたいときにできます。
- 実態は cdk コマンドの wrapper となってるらしい。
- 無料枠だと、動かせるサービスに制限があるので、導入できない場合はローカル環境では Docker compose で別サービスに切り出して検証できるようにするのがいいかも

```
// 例
fino local deploy Sample-Stack
```
