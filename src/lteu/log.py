"""Logging and console module."""

from collections.abc import Iterable
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

CONSOLE = Console()


def print_title(title: str) -> None:
    """Print command title."""
    CONSOLE.print(
        Panel(f"[bold]{title}[/bold]"),
    )


def print_inputs(inputs: Iterable[str]) -> None:
    """Print inputs."""
    CONSOLE.print(
        Panel(
            "\n".join(inputs),
            title="[bold]Inputs[/bold]",
            title_align="left",
        ),
    )


def print_msg(msg: str) -> None:
    """Print message."""
    CONSOLE.print(msg)


def print_done(msg: str) -> None:
    """Print done message."""
    CONSOLE.print(f":white_check_mark: [green]{msg}[/green]")


def print_info(msg: str) -> None:
    """Print info message."""
    CONSOLE.print(f":information: [blue]{msg}[/blue]")


def print_warning(msg: str) -> None:
    """Print warning message."""
    CONSOLE.print(f":warning: [yellow]{msg}[/yellow]")


def print_error(msg: str) -> None:
    """Print error message."""
    CONSOLE.print(f":x: [red]{msg}[/red]")


def fmt_dir(path: Path) -> str:
    """Format directory path for print."""
    return f":file_folder: [bold]{path}[/bold]"


def fmt_file(path: Path) -> str:
    """Format file path for print."""
    return f":page_facing_up: [bold]{path}[/bold]"


def fmt_tool(tool: str) -> str:
    """Format tool for print."""
    return f":hammer_and_wrench: [bold]{tool}[/bold]"


def fmt_img(path: Path) -> str:
    """Format image path for print."""
    return f":bar_chart: [bold]{path}[/bold]"


def fmt_with_chr_input(with_chromosomes: bool) -> str:  # noqa: FBT001
    """Format with chromosomes input for print."""
    if with_chromosomes:
        return ":microbe: With chromosomal bin"
    return ":microbe: Only plasmid bins"
