"""Distribution figures for uniqify ground truths."""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from lteu.eval import measures
from lteu.eval.run import files as eval_files

from . import data as dist_data

if TYPE_CHECKING:
    from pathlib import Path

    from lteu.figs import aes


class Columns(StrEnum):
    """DataFrame columns."""

    SAMPLE_ID = eval_files.Header.SAMPLE_ID
    CONTENT = "Content"
    MEASURE_CLASS = "Measure class"
    MEASURE_MODE = "Measure mode"
    VALUE = "Value"
    HUE = "hue"


class HueValues(StrEnum):
    """Hue values."""

    COMPLETENESS_ONLY_PLASMIDS = (
        f"{measures.Class.COMPLETENESS}-{dist_data.Contents.ONLY_PLASMIDS}"
    )
    COMPLETENESS_WITH_CHROMOSOMES = (
        f"{measures.Class.COMPLETENESS}-{dist_data.Contents.WITH_CHROMOSOMES}"
    )
    HOMOGENEITY_ONLY_PLASMIDS = (
        f"{measures.Class.HOMOGENEITY}-{dist_data.Contents.ONLY_PLASMIDS}"
    )
    HOMOGENEITY_WITH_CHROMOSOMES = (
        f"{measures.Class.HOMOGENEITY}-{dist_data.Contents.WITH_CHROMOSOMES}"
    )

    @classmethod
    def from_measure_and_content(
        cls,
        measure: measures.Class,
        content: dist_data.Contents,
    ) -> HueValues:
        """Get hue value from measure and content."""
        match measure:
            case measures.Class.COMPLETENESS:
                match content:
                    case dist_data.Contents.ONLY_PLASMIDS:
                        return cls.COMPLETENESS_ONLY_PLASMIDS
                    case dist_data.Contents.WITH_CHROMOSOMES:
                        return cls.COMPLETENESS_WITH_CHROMOSOMES
            case measures.Class.HOMOGENEITY:
                match content:
                    case dist_data.Contents.ONLY_PLASMIDS:
                        return cls.HOMOGENEITY_ONLY_PLASMIDS
                    case dist_data.Contents.WITH_CHROMOSOMES:
                        return cls.HOMOGENEITY_WITH_CHROMOSOMES


def get_dataframe(
    only_plm_eval_tsv: Path,
    with_chm_eval_tsv: Path,
) -> pd.DataFrame:
    """Get the dataframe for a distribution figure for ground truths."""
    only_plm_df = eval_files.to_dataframe(only_plm_eval_tsv)
    with_chm_df = eval_files.to_dataframe(with_chm_eval_tsv)

    df = pd.DataFrame(columns=list(Columns))

    for content, eval_df in (
        (dist_data.Contents.ONLY_PLASMIDS, only_plm_df),
        (dist_data.Contents.WITH_CHROMOSOMES, with_chm_df),
    ):
        new_eval_df = dist_data.replace_measures_cols_to_class_mode_val_cols(
            eval_df,
            [eval_files.Header.SAMPLE_ID],
            Columns.MEASURE_CLASS,
            Columns.MEASURE_MODE,
            Columns.VALUE,
        )

        new_eval_df[Columns.CONTENT] = content

        df = pd.concat([df, new_eval_df], ignore_index=True)

    df[Columns.HUE] = df.apply(
        lambda row: HueValues.from_measure_and_content(
            row[Columns.MEASURE_CLASS],
            row[Columns.CONTENT],
        ),
        axis=1,
    )
    return df


class Orders:
    """Orders."""

    def __init__(
        self,
        row: list[measures.Class],
        col: list[measures.Mode],
        x: list[dist_data.Contents],
        hue: list[HueValues],
    ) -> None:
        self._row: list[measures.Class] = row
        self._col: list[measures.Mode] = col
        self._x: list[dist_data.Contents] = x
        self._hue: list[HueValues] = hue

    def row(self) -> list[measures.Class]:
        """Get row."""
        return self._row

    def col(self) -> list[measures.Mode]:
        """Get column."""
        return self._col

    def x(self) -> list[dist_data.Contents]:
        """Get x."""
        return self._x

    def hue(self) -> list[HueValues]:
        """Get hue."""
        return self._hue


class Aes:
    """Distributions aesthetics."""

    def __init__(
        self,
        base_aes: aes.Base,
        orders: Orders,
    ) -> None:
        self._base_aes: aes.Base = base_aes
        self._orders: Orders = orders

    def base(self) -> aes.Base:
        """Get base aesthetic configuration."""
        return self._base_aes

    def orders(self) -> Orders:
        """Get orders."""
        return self._orders


def violins_plot(
    df: pd.DataFrame,
    aes_cfg: Aes,
    pdf: Path,
) -> None:
    """Create a violins plot for ground truths."""
    sns.set_context(aes_cfg.base().context())  # ty:ignore[invalid-argument-type]

    g = sns.catplot(
        data=df,
        y=Columns.VALUE,
        # FacedGrid
        kind="violin",
        row=Columns.MEASURE_CLASS,
        row_order=aes_cfg.orders().row(),
        col=Columns.MEASURE_MODE,
        col_order=aes_cfg.orders().col(),
        sharex=True,
        sharey=True,
        margin_titles=True,
        legend=False,
        # Violinplot options
        x=Columns.CONTENT,
        hue=Columns.HUE,
        order=aes_cfg.orders().x(),
        hue_order=aes_cfg.orders().hue(),
        palette="Paired",
        bw_adjust=0.5,
        cut=1,
        linewidth=1,
        fill=True,
    )
    n_samples = df[Columns.SAMPLE_ID].nunique()
    #
    # Title
    #
    g.figure.suptitle(
        ""
        if aes_cfg.base().focus()
        else (
            "Evaluation measures for original ground truths against themselves"
            f"\n({n_samples} samples)"
        ),
    )
    #
    # Subplot titles
    #
    g.set_titles(col_template="{col_name}", row_template="{row_name}")

    g.set_xlabels("")
    g.set_ylabels("")
    #
    # Sub X axis tick labels
    #
    g.set_xticklabels(
        labels=[content.to_label() for content in aes_cfg.orders().x()],
        ha="center",
    )
    g.tight_layout()

    g.savefig(pdf)
    plt.close()
