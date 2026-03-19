"""Figures applications."""

import typer

from .distribution import app as dist_app
from .versus import app as versus_app

APP = typer.Typer(name="figs", help="Figures commands.")

APP.add_typer(versus_app.APP)
APP.add_typer(dist_app.APP)
