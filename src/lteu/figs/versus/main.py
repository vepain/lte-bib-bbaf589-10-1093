"""Versus figures."""

import enum
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from lteu.figs import aes, items

CLASS_COL = "Class"


class Class(enum.StrEnum):
    """Class values."""

    ABOVE = "Above"
    EQUAL = "Equal"
    BELOW = "Below"


def add_class_column(df: pd.DataFrame, x_col: str, y_col: str) -> pd.DataFrame:
    """Add a class column to a dataframe."""

    # class column is either Below, Equal or Above the diagonal
    def _class_value(row: pd.Series) -> str:
        if row[x_col] > row[y_col]:
            return Class.BELOW
        if row[x_col] < row[y_col]:
            return Class.ABOVE
        return Class.EQUAL

    df[CLASS_COL] = df.apply(_class_value, axis=1)

    return df


class Labels:
    """Labels for a versus figure."""

    def __init__(
        self,
        title: str,
        x_label: str,
        y_label: str,
    ) -> None:
        self._title: str = title
        self._x_label: str = x_label
        self._y_label: str = y_label

    def title(self) -> str:
        """Get title."""
        return self._title

    def x(self) -> str:
        """Get x label."""
        return self._x_label

    def y(self) -> str:
        """Get y label."""
        return self._y_label


class Aes:
    """Aeshetics for a versus figure."""

    def __init__(
        self,
        base_cfg: aes.Base,
        labels: Labels,
    ) -> None:
        self._base_cfg: aes.Base = base_cfg
        self._labels: Labels = labels

    def base(self) -> aes.Base:
        """Get the base configuration."""
        return self._base_cfg

    def labels(self) -> Labels:
        """Get the labels configuration."""
        return self._labels


def gt(
    df: pd.DataFrame,
    aes_cfg: Aes,
    pdf_path: Path,
) -> None:
    """Create a versus figure for ground truths."""
    sns.set_context(aes_cfg.base().context())  # ty:ignore[invalid-argument-type]

    fig, ax = plt.subplots(figsize=(6, 6))
    sns.scatterplot(
        data=df,
        x=items.Versions.V1,
        y=items.Versions.V2,
        hue=CLASS_COL,
        hue_order=[Class.ABOVE, Class.EQUAL, Class.BELOW],
        palette="Set3",
        ax=ax,
        zorder=2,
    )

    def final_aes() -> None:
        #
        # Add diagonal in background
        #
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        lims = [max(x0, y0), min(x1, y1)]
        ax.plot(
            lims,
            lims,
            color="grey",
            linewidth=1,
            linestyle="-",
            alpha=0.8,
            zorder=1,
        )
        #
        # Legends
        #
        ax.set_title("" if aes_cfg.base().focus() else f"{aes_cfg.labels().title()}")

        ax.set_xlabel(f"{aes_cfg.labels().x()}\n(n = {df.shape[0]})")
        ax.set_ylabel(aes_cfg.labels().y())

    final_aes()

    fig.savefig(pdf_path)
    plt.close()
