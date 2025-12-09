from enum import Enum

import typer
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True)


class Target(str, Enum):
    EDINET = "edinet"
    TDNET = "tdnet"


@app.command()
def collect(
    target: Annotated[
        Target,
        typer.Option(
            "--target",
            "-t",
            case_sensitive=False,
            help="Target system name to collect data",
        ),
    ] = "edinet",
):
    """
    Collect data from the target system.
    """
    print(target.value)


if __name__ == "__main__":
    app()
