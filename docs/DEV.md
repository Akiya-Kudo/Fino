# プロジェクトセットアップ

cd fino
uv sync --all-packages

# 開発時の依存関係インストール

uv pip install -e packages/fino-core[dev] ⇦ うまくいかん
uv pip install -e packages/fino-cli[dev]　 ⇦ うまくいかん

# Linting & Formatting

uv run ruff check .
uv run ruff format .

# テスト実行

uv run pytest packages/fino-core/tests
uv run pytest packages/fino-cli/tests

# CLI の動作確認

uv run fino --help
