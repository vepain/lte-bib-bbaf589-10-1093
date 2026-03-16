"""Typer module."""

import typer

from .eval import app as eval_app
from .fmt import app as fmt_app
from .uniqify import app as uniqify_app

APP = typer.Typer(help="Letter To the Editor Utilities.")

APP.add_typer(fmt_app.APP)
APP.add_typer(eval_app.APP)
APP.add_typer(uniqify_app.APP)
