# ===============================
# Makefile for Fino
# ===============================
# .envの環境変数を読み込む
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# ===============================
# CDK Makefile
# ===============================

DEFAULT_PROFILE ?= $(AWS_PROFILE)
LOCAL_PROFILE   ?= $(LOCALSTACK_PROFILE)

# AWS_ACCOUNT_ID ?= $(AWS_ACCOUNT_ID)
# LOCALSTACK_ACCOUNT_ID ?= 000000000000

CDK      = cdk
CDKLOCAL = cdklocal

RUN_CDK = cd infra &&

# Extract extra args:
# Remove the make target name from MAKECMDGOALS
ARGS = $(filter-out $@,$(MAKECMDGOALS))

# Avoid "No rule to make target" errors for args
%:
	@:

# -------- Default AWS --------
deploy:
	$(RUN_CDK) $(CDK) deploy --profile $(DEFAULT_PROFILE) $(ARGS) 

synth:
	$(RUN_CDK) $(CDK) synth --profile $(DEFAULT_PROFILE) $(ARGS)

diff:
	$(RUN_CDK) $(CDK) diff --profile $(DEFAULT_PROFILE) $(ARGS)

destroy:
	$(RUN_CDK) $(CDK) destroy --profile $(DEFAULT_PROFILE) $(ARGS)

bootstrap:
	$(RUN_CDK) $(CDK) bootstrap --profile $(DEFAULT_PROFILE) $(ARGS)

# -------- LocalStack --------
local-deploy:
	$(RUN_CDK) $(CDKLOCAL) deploy --profile $(LOCAL_PROFILE) $(ARGS)

local-synth:
	$(RUN_CDK) $(CDKLOCAL) synth --profile $(LOCAL_PROFILE) $(ARGS)

local-diff:
	$(RUN_CDK) $(CDKLOCAL) diff --profile $(LOCAL_PROFILE) $(ARGS)

local-destroy:
	$(RUN_CDK) $(CDKLOCAL) destroy --profile $(LOCAL_PROFILE) $(ARGS)

local-bootstrap:
	$(RUN_CDK) $(CDKLOCAL) bootstrap --profile $(LOCAL_PROFILE) $(ARGS)

# -------- Setup --------

setup:
	$(RUN_CDK) scripts/setup.sh

# -------- Test --------

test:
	$(RUN_CDK) npm run test

echo:
	@echo "$(LOCALSTACK_MOUNT_DIR)"