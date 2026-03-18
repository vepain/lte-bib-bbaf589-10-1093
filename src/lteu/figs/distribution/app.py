"""Distribution plots applications."""

import typer

APP = typer.Typer(name="dist", help="Distribution plots commands.")


class InputsUniqifyGT:
    """Inputs for gt command."""


@APP.command(name="uniqify-gt")
def uniqify_gt() -> None:
    """Uniqify versus ground truths."""
    raise NotImplementedError
