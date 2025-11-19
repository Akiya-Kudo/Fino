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
# 引数の1つ目をCDKサブコマンドとして使用
# 使用例: make cdk deploy, make cdk synth, make cdk destroy など
cdk:
	@if [ -z "$(word 1,$(ARGS))" ]; then \
		echo "Error: CDK subcommand is required. Usage: make cdk <subcommand> [args...]"; \
		echo "Available subcommands: deploy, synth, diff, destroy, bootstrap, ls, list, etc."; \
		exit 1; \
	fi
	$(RUN_CDK) $(CDK) $(word 1,$(ARGS)) --profile $(DEFAULT_PROFILE) $(filter-out $(word 1,$(ARGS)),$(ARGS))


# -------- LocalStack --------
# 引数の1つ目をCDKサブコマンドとして使用
# 使用例: make local deploy, make local synth, make local destroy など
local:
	@if [ -z "$(word 1,$(ARGS))" ]; then \
		echo "Error: CDK subcommand is required. Usage: make local <subcommand> [args...]"; \
		echo "Available subcommands: deploy, synth, diff, destroy, bootstrap, ls, list, etc."; \
		exit 1; \
	fi
	$(RUN_CDK) $(CDKLOCAL) $(word 1,$(ARGS)) --profile $(LOCAL_PROFILE) $(filter-out $(word 1,$(ARGS)),$(ARGS))


# -------- Setup --------

setup:
	$(RUN_CDK) scripts/setup.sh

# -------- Test --------

test:
	$(RUN_CDK) npm run test

echo:
	@echo "$(LOCALSTACK_VOLUME_DIR)"