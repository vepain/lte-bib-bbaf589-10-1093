"""Formatting module."""

import typer

APP = typer.Typer(name="fmt", help="Formatting files.")


@APP.command("gt-to-plaseval")
def gt_to_plaseval() -> None:
    """Format paper ground truth to PlasEval ground truth."""
