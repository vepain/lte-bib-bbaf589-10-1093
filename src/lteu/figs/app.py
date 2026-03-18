"""Figures applications."""

import typer

from .uniqify import app as uniqify_app

APP = typer.Typer(name="figs", help="Figures commands.")

APP.add_typer(uniqify_app.APP)
