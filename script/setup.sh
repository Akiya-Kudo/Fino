#! /bin/bash

# sourceで読み込むと元のプロセス自体がエラーとなり、プロセスが終了してしまうため、コメントアウト
# set -e

### FINO PROJECT ###
echo "Setup Fino Project"
echo "================================================"
echo "process: add alias fino='make'"
alias fino="make"

### INFA ####
# Create AWS Account

# Create AWS API Key
# @see https://docs.localstack.cloud/aws/integrations/aws-native-tools/aws-cli/

# Setup awscli (with the API Key)
# @see https://docs.localstack.cloud/aws/integrations/aws-native-tools/aws-cdk/

# Setup aws-cdk

# Setup awscli-local

# Setup aws-cdk-local

# npm install
echo "process: npm install cdk dependencies (infra)"
cd infra/cdk && npm install && cd ../..
