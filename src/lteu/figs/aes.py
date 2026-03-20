"""Figure aesthetics."""

from enum import StrEnum

import typer


class TyperInputs:
    """Aeshetics typer inputs."""

    CONTEXT = typer.Option(
        "--context",
        "-c",
        help="Seaborn context",
    )
    FOCUS = typer.Option(
        ("--focus/--full"),
        help="Focus mode (without title etc.)",
    )


class SeabornContext(StrEnum):
    """Seaborn contexts."""

    PAPER = "paper"
    NOTEBOOK = "notebook"
    TALK = "talk"
    POSTER = "poster"


class Base:
    """Base aesthetics."""

    DEF_CONTEXT: SeabornContext = SeabornContext.NOTEBOOK
    DEF_FOCUS = False

    def __init__(
        self,
        context: SeabornContext,
        focus: bool,  # noqa: FBT001
    ) -> None:
        self._context: SeabornContext = context
        self._focus: bool = focus

    def context(self) -> SeabornContext:
        """Get context."""
        return self._context

    def focus(self) -> bool:
        """Get focus."""
        return self._focus
