from enum import Enum

import rich
import typer
from click.core import ParameterSource
from typing_extensions import Annotated

from command.utils import FinoColors

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
    # edinet_api_key: Annotated[str, typer.Option()]
):
    """
    Collect data from the target system.
    """
    if ctx.get_parameter_source("target") == ParameterSource.DEFAULT:
        rich.print(
            f"[{FinoColors.MAGENTA3}]Since target option is not specified, data will be collected from the default Edinet[/{FinoColors.MAGENTA3}]"
        )


if __name__ == "__main__":
    app()
