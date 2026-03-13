"""Typer module."""

import typer

from . import format as fmt
from .eval import app as eval_app

APP = typer.Typer(help="Letter To the Editor Utilities.")

APP.add_typer(fmt.APP)
APP.add_typer(eval_app.APP)
