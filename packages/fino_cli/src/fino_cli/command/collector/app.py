from enum import Enum

import rich
import typer
from click.core import ParameterSource
from fino_cli.config import settings
from fino_cli.util.theme import FinoColors
from fino_core import collect_edinet
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True)


class Target(str, Enum):
    EDINET = "edinet"
    TDNET = "tdnet"


@app.command()
def collector(
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
    edinet_api_key: Annotated[str, typer.Option()] = settings.get(
        "EDINET__API_KEY", default=""
    ),
) -> None:
    """
    Collect data from the target system.
    """
    # paramter check
    if ctx.get_parameter_source("target") == ParameterSource.DEFAULT:
        rich.print(
            f"[{FinoColors.ORANGE3}]Since target option is not specified, data will be collected from the default Edinet[/{FinoColors.ORANGE3}]"
        )

    # parameter validation
    if edinet_api_key == "":
        raise typer.BadParameter(
            "edinet api key is not set. please set in config file or environment variable."
        )

    # fino core collector
    collect_edinet()


if __name__ == "__main__":
    app()
