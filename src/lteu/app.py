"""Typer module."""

import typer

from . import format as fmt

APP = typer.Typer(help="Letter To the Editor Utilities.")

APP.add_typer(fmt.APP)
