"""Figures applications."""

import typer

from .versus import app as vs_app

APP = typer.Typer(name="figs", help="Figures commands.")

APP.add_typer(vs_app.APP)
