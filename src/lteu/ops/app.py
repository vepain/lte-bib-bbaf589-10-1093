"""Operations application."""

import typer

from .uniqify import app as uniqify_app

APP = typer.Typer(name="ops", help="Operations commands.")


APP.add_typer(uniqify_app.APP)
