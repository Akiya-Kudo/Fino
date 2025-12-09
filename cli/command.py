import typer

from command.kamino.command import app as kamino

app = typer.Typer(no_args_is_help=True)

app.add_typer(kamino, name="kamino")


@app.command()
def main():
    """
    Say hi to the world.
    """
    print("Hello, World!")


if __name__ == "__main__":
    app()
