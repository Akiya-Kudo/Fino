import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def collect():
    """
    Collect data from the source.
    """
    print("Collecting data from the source...")


if __name__ == "__main__":
    app()
