"""Evaluation applications."""

import typer

from .merge import app as merge_app
from .run import app as run_app

APP = typer.Typer(name="eval", help="Evaluation commands.")

APP.add_typer(run_app.APP)
APP.add_typer(merge_app.APP)
