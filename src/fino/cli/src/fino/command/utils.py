"""CLI共通ユーティリティ関数と定数"""

from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel

# ===============================
# 色コード定数
# ===============================


class FinoColors:
    """Fino CLIで使用する色コード定数（Rich標準色名ベース）"""

    # Red系
    LIGHT_SALMON3 = "#d7875f"
    # Pink系
    DEEP_PINK3 = "#d70087"
    # Magenta/Purple系
    MAGENTA3 = "#d700d7"

    # Orange系
    ORANGE3 = "#d78700"

    # Gold/Yellow系
    GOLD3 = "#d7af00"
    YELLOW3 = "#d7d700"
    # Rose系
    MISTY_ROSE3 = "#d7afaf"
    # Blue/Cyan系
    LIGHT_STEEL_BLUE1 = "#d7d7ff"
    LIGHT_CYAN1 = "#d7ffff"

    # ERROR
    ERROR = "#d70000"
    # SUCCESS
    SUCCESS = "#00d700"
    # INFO
    INFO = "#d78700"
    # WARNING
    WARNING = "#d7d700"


# ===============================
# パネル表示ユーティリティ
# ===============================

console = Console()


@dataclass
class PanelConfig:
    """パネル表示の設定"""

    title: str
    content: str
    border_style: str = FinoColors.GOLD3
    fit: bool = True


def print_panel(
    content: str,
    title: str,
    border_style: str = FinoColors.GOLD3,
    fit: bool = True,
) -> None:
    """
    共通のパネル表示関数

    Args:
        content: パネルに表示するコンテンツ（Richマークアップ対応）
        title: パネルのタイトル
        border_style: ボーダーの色（デフォルト: ゴールド）
        fit: パネルをフィットさせるかどうか（デフォルト: True）
    """
    panel = (
        Panel.fit(content, title=title, border_style=border_style)
        if fit
        else Panel(content, title=title, border_style=border_style)
    )
    console.print(panel)


def print_error(message: str) -> None:
    """
    エラーメッセージを表示

    Args:
        message: エラーメッセージ
    """
    console.print(f"[{FinoColors.ERROR}]Error:[/{FinoColors.ERROR}] {message}")


def print_success(message: str) -> None:
    """
    成功メッセージを表示

    Args:
        message: 成功メッセージ
    """
    console.print(
        f"[{FinoColors.SUCCESS}]Success:[/{FinoColors.SUCCESS}] {message}"
    )


def print_info(message: str) -> None:
    """
    情報メッセージを表示

    Args:
        message: 情報メッセージ
    """
    console.print(f"[{FinoColors.INFO}]Info:[/{FinoColors.INFO}] {message}")


def print_warning(message: str) -> None:
    """
    警告メッセージを表示

    Args:
        message: 警告メッセージ
    """
    console.print(
        f"[{FinoColors.WARNING}]Warning:[/{FinoColors.WARNING}] {message}"
    )
