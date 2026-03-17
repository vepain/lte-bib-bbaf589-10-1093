"""Figure aesthetics."""

from enum import StrEnum

import typer

from lteu import tools
from lteu.figs import items, ops


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

    DEF_CONTEXT = SeabornContext.NOTEBOOK
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


class Tools:
    """Tools aesthetics."""

    def __init__(
        self,
        remove_samples: ops.RmSamplesModes,
        tools_order: list[tools.Binning],
    ) -> None:
        self._remove_samples: ops.RmSamplesModes = remove_samples
        self._tools_order: list[tools.Binning] = tools_order

    def remove_samples(self) -> ops.RmSamplesModes:
        """Get remove samples mode."""
        return self._remove_samples

    def tools_order(self) -> list[tools.Binning]:
        """Get methods order."""
        return self._tools_order

    def tool_palette(self) -> list[tuple[float, float, float]]:
        """Get method palette."""
        return items.tools_color_palette(self.tools_order())
