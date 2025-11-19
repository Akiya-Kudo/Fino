#! /bin/bash

# sourceで読み込むと元のプロセス自体がエラーとなり、プロセスが終了してしまうため、コメントアウト
# set -e

### FINO PROJECT ###
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
cd infra && npm install && cd ..
