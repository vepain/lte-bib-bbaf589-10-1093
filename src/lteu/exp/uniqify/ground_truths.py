"""Uniqify ground truths experiment."""

from pathlib import Path

import typer

APP = typer.Typer(name="gt", help="Uniqify ground truths experiment.")


class Inputs:
    """Experiment inputs."""

    DATA_DIR = typer.Argument(
        help="Path to the data directory.",
    )


class FileSystem:
    """Experiment file system."""

    EXP_RELPATH = Path("uniqify/ground_truths")

    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir

    def data_dir(self) -> Path:
        """Get data directory."""
        return self._data_dir

    def exp_dir(self) -> Path:
        """Get experiment directory."""
        return self._data_dir / self.EXP_RELPATH


# def init() -> None:
