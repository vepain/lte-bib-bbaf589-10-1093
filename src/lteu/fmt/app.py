"""Formatting module."""

import typer

from .plaseval import app as pe_app
from .samples import app as smp_app

APP = typer.Typer(name="fmt", help="Formatting commands.")

APP.add_typer(pe_app.APP)
APP.add_typer(smp_app.APP)
