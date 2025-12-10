from enum import Enum

import rich
import typer
from click.core import ParameterSource
from typing_extensions import Annotated

from command.utils import FinoColors
from config import settings

app = typer.Typer(no_args_is_help=True)


class Target(str, Enum):
    EDINET = "edinet"
    TDNET = "tdnet"


@app.command()
def collect(
    ctx: typer.Context,
    target: Annotated[
        Target,
        typer.Option(
            "--target",
            "-t",
            case_sensitive=False,
            help="Target system name to collect data",
        ),
    ] = "edinet",
    edinet_api_key: Annotated[
        str, typer.Option(envvar="FINO_EDINET_API_KEY")
    ] = settings.get("FINO_EDINET_API_KEY", default=""),
):
    """
    Collect data from the target system.
    """
    # drfault value check and validation
    if ctx.get_parameter_source("target") == ParameterSource.DEFAULT:
        rich.print(
            f"[{FinoColors.MAGENTA3}]Since target option is not specified, data will be collected from the default Edinet[/{FinoColors.MAGENTA3}]"
        )
    if edinet_api_key == "":
        raise typer.BadParameter(
            "edinet api key is not set. please set in config file or environment variable."
        )
    print("edinet api key is :", edinet_api_key)


if __name__ == "__main__":
    app()
