#! /bin/bash

set -e

# Create AWS Account

# Create AWS API Key
# @see https://docs.localstack.cloud/aws/integrations/aws-native-tools/aws-cli/

# Setup awscli (with the API Key)
# @see https://docs.localstack.cloud/aws/integrations/aws-native-tools/aws-cdk/

# Setup aws-cdk

# Setup awscli-local

# Setup aws-cdk-local

# Setup Locakstack
export AWS_PROFILE=localstack



##################################
########## Setup direnv ##########
##################################
echo "=== Direnv Setup Script ==="

# Detect shell
CURRENT_SHELL=$(basename "$SHELL")
echo "Detected shell: $CURRENT_SHELL"

# Determine rc file
if [ "$CURRENT_SHELL" = "bash" ]; then
    RC_FILE="$HOME/.bashrc"
    HOOK_CMD='eval "$(direnv hook bash)"'
elif [ "$CURRENT_SHELL" = "zsh" ]; then
    RC_FILE="$HOME/.zshrc"
    HOOK_CMD='eval "$(direnv hook zsh)"'
elif [ "$CURRENT_SHELL" = "fish" ]; then
    RC_FILE="$HOME/.config/fish/config.fish"
    HOOK_CMD='eval (direnv hook fish)'
else
    echo "Unsupported shell: $CURRENT_SHELL"
    echo "Supported: bash, zsh, fish"
    exit 1
fi

echo "Using RC file: $RC_FILE"

# Install direnv if not found
if ! command -v direnv >/dev/null 2>&1; then
    echo "direnv not found, installing..."
    TMP_DIR=$(mktemp -d)
    cd "$TMP_DIR"

    git clone https://github.com/direnv/direnv
    cd direnv
    sudo make install

    echo "direnv installed."
else
    echo "direnv already installed."
fi

# Add hook if missing
if ! grep -Fxq "$HOOK_CMD" "$RC_FILE"; then
    echo "Adding direnv hook to $RC_FILE"
    echo "" >> "$RC_FILE"
    echo "# Added by direnv setup script" >> "$RC_FILE"
    echo "$HOOK_CMD" >> "$RC_FILE"
else
    echo "Direnv hook already exists in $RC_FILE"
fi

echo "=== Setup Complete ==="
echo "Please restart your terminal or run: source $RC_FILE"
