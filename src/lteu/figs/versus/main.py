"""Versus figures."""

import enum
from pathlib import Path
from typing import assert_never

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from lteu.figs import aes, items, ops

CLASS_COL = "Class"


class Class(enum.StrEnum):
    """Class values."""

    ABOVE = "Above"
    EQUAL = "Equal"
    BELOW = "Below"


def get_dataframe_gt(
    x_evals_tsv: Path,
    y_evals_tsv: Path,
    measure: items.MeasureCodes,
    remove_samples: ops.RmSamplesModes,
) -> pd.DataFrame:
    """Get the dataframe for a versus figure for ground truths."""
    df = ops.get_gt_evals(x_evals_tsv, y_evals_tsv, remove_samples)

    # Keep only intersection samples between the two versions
    match remove_samples:
        case ops.RmSamplesModes.FAILS:
            pass  # Already done before
        case ops.RmSamplesModes.NOTHING:
            df = ops.remove_samples_with_nan(df)
        case _:
            assert_never(remove_samples)

    df = pd.pivot_table(
        df,
        index=items.Header.SAMPLE_ID,
        columns=items.Header.VERSION,
        values=measure.to_column(),
    )

    # class column is either Below, Equal or Above the diagonal
    def _class_value(row: pd.Series) -> str:
        if row[items.Versions.V1] > row[items.Versions.V2]:
            return Class.BELOW
        if row[items.Versions.V1] < row[items.Versions.V2]:
            return Class.ABOVE
        return Class.EQUAL

    df[CLASS_COL] = df.apply(_class_value, axis=1)

    return df


class Labels:
    """Labels for a versus figure."""

    def __init__(
        self,
        x_label: str,
        y_label: str,
    ) -> None:
        self._x_label: str = x_label
        self._y_label: str = y_label

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
    measure: items.MeasureCodes,
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
        ax.set_title("" if aes_cfg.base().focus() else f"{measure.to_label('plural')}")

        ax.set_xlabel(f"{aes_cfg.labels().x()}\n(n = {df.shape[0]})")
        ax.set_ylabel(aes_cfg.labels().y())

    final_aes()

    fig.savefig(pdf_path)
    plt.close()
