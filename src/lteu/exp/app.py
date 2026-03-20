"""Experiments applications."""

import typer

from . import init

APP = typer.Typer(name="exp", help="Experiments commands.")

APP.add_typer(init.APP)
