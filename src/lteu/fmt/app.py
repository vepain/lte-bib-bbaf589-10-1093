"""Formatting module."""

import typer

from .merge_eval import app as me_app
from .plaseval import app as pe_app
from .samples import app as smp_app

APP = typer.Typer(name="fmt", help="Formatting commands.")

APP.add_typer(pe_app.APP)
APP.add_typer(smp_app.APP)
APP.add_typer(me_app.APP)
