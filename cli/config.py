from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="FINO",
    environments=False,
    load_dotenv=True,
    dotenv_path="../",
    settings_files=["../settings.toml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
