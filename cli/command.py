import rich
import typer
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True)

data = {
    "name": "Rick",
    "age": 42,
    "items": [{"name": "Portal Gun"}, {"name": "Plumbus"}],
    "active": True,
    "affiliation": None,
}


@app.command()
def main(
    name: str,
    formal: Annotated[
        bool, typer.Option(prompt=True, help="Say hi very formally.")
    ] = False,
):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    # if formal:
    #     print(f"Good day Ms. {name} {lastname}.")
    # else:
    #     print(f"Hello {name} {lastname}")
    rich.print(
        "[bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:"
    )
    raise typer.Exit(code=1)
    rich.print(data)


if __name__ == "__main__":
    app()
