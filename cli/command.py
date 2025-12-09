import typer
from rich.console import Console
from rich.panel import Panel

from command.kamino.command import app as kamino

console = Console()


app = typer.Typer(invoke_without_command=True, no_args_is_help=False)

app.add_typer(
    kamino,
    name="kamino",
    help="Kamino is a ingestion workflow and raw data storage.",
)


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    # コマンドが指定されている場合はパネルを表示しない
    if ctx.invoked_subcommand is not None:
        return

    # コマンドなしで実行された場合のみオンボーディングパネルを表示
    console.print(
        Panel.fit(
            """[bold #ff5f00]Fino CLI[/bold #ff5f00] - Financial data management CLI tool -
            [bold #ff875f]Fino[/bold #ff875f] is a powerful financial data platform for supporting your investment decisions.
            
            [bold #ffafd7]Features:[/bold #ffafd7]
            - raw data ingestion workflow.
            - data-lakehouse management.

            [#ffd700]***[/#ffd700] please check --help option what you can do with fino cli [#ffd700]***[/#ffd700]

            (— This Project service-names are inspired by Star Wars planets! :stars: )
            """,
            title="🚀 Welcome Fino CLI",
            border_style="#ffd700",
        )
    )


if __name__ == "__main__":
    app()
