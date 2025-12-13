import typer
from fino-cli.util.theme import FinoColors
from rich.console import Console
from rich.panel import Panel

console = Console()

app = typer.Typer(
    name="fino", invoke_without_command=True, no_args_is_help=False
)

# app.add_typer(
#     kamino,
#     name="kamino",
#     help="Kamino is a ingestion workflow and raw data storage.",
# )


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context) -> None:
    # コマンドが指定されている場合はパネルを表示しない
    if ctx.invoked_subcommand is not None:
        return

    # コマンドなしで実行された場合のみオンボーディングパネルを表示
    console.print(
        Panel.fit(
            f"""[bold {FinoColors.ORANGE3}]Fino CLI[/bold {FinoColors.ORANGE3}] - Financial data management CLI tool -
            [bold {FinoColors.LIGHT_SALMON3}]Fino[/bold {FinoColors.LIGHT_SALMON3}] is a powerful financial data platform for supporting your investment decisions.

            [bold {FinoColors.DEEP_PINK3}]Features:[/bold {FinoColors.DEEP_PINK3}]
            - raw data ingestion workflow.
            - data-lakehouse management.

            [{FinoColors.GOLD3}]***[/{FinoColors.GOLD3}] please check --help option what you can do with fino cli [{FinoColors.GOLD3}]***[/{FinoColors.GOLD3}]

            (— This Project service-names are inspired by Star Wars planets! :stars: )
            """,
            title="🚀 Welcome Fino CLI",
            border_style=FinoColors.GOLD3,
        )
    )


if __name__ == "__main__":
    app()
