"""Uniqify experiments figures applications."""

import typer

from .gt import app as gt_app

APP = typer.Typer(name="uniqify", help="Uniqify experiments figures commands.")

APP.add_typer(gt_app.APP)
