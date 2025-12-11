import os

from dynaconf import Dynaconf

"""
# Dynaconf の設定読み込み挙動メモ

- settings.toml / settings.yaml などの設定ファイルはsettings_files に指定したパスを確認する。
    - 相対pathを使用できる
    - 親ディレクトリの探索を行う
    - 優先順位は settings_files 指定dirに近いものが優先される。

- root_pathを指定した場合、それを元に上記の探索を行われる
- root_path を明示しない場合、Dynaconf を初期化したディレクトリ（settings.py）が基準になり、上記の探索が行われる
    - CLI 実行ディレクトリには依存しないが、サブディレクトリで初期化すると設定ファイルの探索位置がズレる。
    - CLI 実行ディレクトリに依存するようにするためにはroot_pathにos.getcwd()を指定する。
"""

root_path = os.getenv("FINO_CONFIG_DIR")

print("root_path", root_path)


settings = Dynaconf(
    envvar_prefix="FINO",
    # The list of enabled loaders that dynaconf will use to load settings files,
    # if your application is using only YAML you can for example change it to ['YAML'] so dynaconf stops trying to load toml and other formats.
    core_loaders=["TOML"],
    # If the specified Dynaconf enters in a GLOBAL MERGE mode and when loading new files or sources will not override but merge data structures by default.
    merge_enabled=True,
    settings_files=["settings.toml", ".secrets.toml"],
    # When turned on, dynaconf will try to load the variables from a .env file.
    load_dotenv=True,
    root_path=root_path,
)
