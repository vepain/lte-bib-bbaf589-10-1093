"""Distribution figures for uniqify ground truths."""

from enum import StrEnum
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from lteu.eval.run import files as eval_files
from lteu.figs import aes
from lteu.figs import items as figs_items


class MeasureClass(StrEnum):
    """Measure class."""

    COMPLETENESS = "Completeness"
    HOMOGENEITY = "Homogeneity"


class MeasureMode(StrEnum):
    """Measure modes."""

    UNWEIGHTED = "Unweighted"
    WEIGHTED = "Weighted"


class Columns(StrEnum):
    """DataFrame columns."""

    SAMPLE_ID = eval_files.Header.SAMPLE_ID
    CONTENT = "Content"
    MEASURE_CLASS = "Measure class"
    MEASURE_MODE = "Measure mode"
    VALUE = "Value"


def get_dataframe(
    only_plm_eval_tsv: Path,
    with_chm_eval_tsv: Path,
) -> pd.DataFrame:
    """Get the dataframe for a distribution figure for ground truths."""
    only_plm_df = eval_files.to_dataframe(only_plm_eval_tsv)
    with_chm_df = eval_files.to_dataframe(with_chm_eval_tsv)

    df = pd.DataFrame(columns=list(Columns))

    for content, eval_df in (
        (figs_items.Contents.ONLY_PLASMIDS, only_plm_df),
        (figs_items.Contents.WITH_CHROMOSOMES, with_chm_df),
    ):
        new_eval_df = eval_df.melt(
            id_vars=[eval_files.Header.SAMPLE_ID],
            value_vars=[
                eval_files.Header.UNW_COMPLETENESS,
                eval_files.Header.W_COMPLETENESS,
                eval_files.Header.UNW_HOMOGENEITY,
                eval_files.Header.W_HOMOGENEITY,
            ],
            var_name="tmp_var",
            value_name=Columns.VALUE,
        )

        # Create two columns according to the value in tmp_var column
        def tmp_var_to_measure_class(
            x: Literal[
                eval_files.Header.UNW_COMPLETENESS,
                eval_files.Header.W_COMPLETENESS,
                eval_files.Header.UNW_HOMOGENEITY,
                eval_files.Header.W_HOMOGENEITY,
            ],
        ) -> MeasureClass:
            match x:
                case (
                    eval_files.Header.UNW_COMPLETENESS
                    | eval_files.Header.W_COMPLETENESS
                ):
                    return MeasureClass.COMPLETENESS
                case (
                    eval_files.Header.UNW_HOMOGENEITY | eval_files.Header.W_HOMOGENEITY
                ):
                    return MeasureClass.HOMOGENEITY

        def tmp_var_to_measure_mode(
            x: Literal[
                eval_files.Header.UNW_COMPLETENESS,
                eval_files.Header.W_COMPLETENESS,
                eval_files.Header.UNW_HOMOGENEITY,
                eval_files.Header.W_HOMOGENEITY,
            ],
        ) -> MeasureMode:
            match x:
                case (
                    eval_files.Header.UNW_COMPLETENESS
                    | eval_files.Header.UNW_HOMOGENEITY
                ):
                    return MeasureMode.UNWEIGHTED
                case eval_files.Header.W_COMPLETENESS | eval_files.Header.W_HOMOGENEITY:
                    return MeasureMode.WEIGHTED

        new_eval_df[Columns.MEASURE_CLASS] = new_eval_df["tmp_var"].apply(
            tmp_var_to_measure_class,
        )
        new_eval_df[Columns.MEASURE_MODE] = new_eval_df["tmp_var"].apply(
            tmp_var_to_measure_mode,
        )
        new_eval_df = new_eval_df.drop(columns=["tmp_var"])

        new_eval_df[Columns.CONTENT] = content

        df = pd.concat([df, new_eval_df], ignore_index=True)

    return df


class TicksOrder:
    """Ticks orders."""

    def __init__(
        self,
        row: list[MeasureClass],
        col: list[MeasureMode],
        x: list[figs_items.Contents],
    ) -> None:
        self._row: list[MeasureClass] = row
        self._col: list[MeasureMode] = col
        self._x: list[figs_items.Contents] = x

    def row(self) -> list[MeasureClass]:
        """Get row."""
        return self._row

    def col(self) -> list[MeasureMode]:
        """Get column."""
        return self._col

    def x(self) -> list[figs_items.Contents]:
        """Get x."""
        return self._x


class Aes:
    """Distributions aesthetics."""

    def __init__(
        self,
        base_aes: aes.Base,
        ticks_order: TicksOrder,
    ) -> None:
        self._base_aes: aes.Base = base_aes
        self._ticks_order: TicksOrder = ticks_order

    def base(self) -> aes.Base:
        """Get base aesthetic configuration."""
        return self._base_aes

    def ticks_order(self) -> TicksOrder:
        """Get ticks order."""
        return self._ticks_order


# class ViolinPlotCfg(TypedDict):
#     """Violin plot config."""

#     x: base.Header
#     hue: base.Header
#     order: list[base.MethodCodes]
#     hue_order: list[base.MethodCodes]
#     palette: list[tuple[float, float, float]]
#     bw_adjust: float
#     cut: int
#     linewidth: int
#     fill: bool


# def new_violin_plot_cfg(
#     aes_cfg: DistributionsAesConfig,
# ) -> ViolinPlotCfg:
#     """Create a new violin plot config."""
#     return ViolinPlotCfg(
#         x=base.Header.METHOD_CODE,
#         hue=base.Header.METHOD_CODE,
#         order=aes_cfg.labels().methods(),
#         hue_order=aes_cfg.labels().methods(),
#         palette=aes_cfg.labels().method_palette(),
#         bw_adjust=0.5,
#         cut=1,
#         linewidth=1,
#         fill=True,
#     )


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
        row_order=aes_cfg.ticks_order().row(),
        col=Columns.MEASURE_MODE,
        col_order=aes_cfg.ticks_order().col(),
        sharex=True,
        sharey=True,
        margin_titles=True,
        # Violinplot options
        x=Columns.CONTENT,
        hue=Columns.CONTENT,
        order=aes_cfg.ticks_order().x(),
        hue_order=aes_cfg.ticks_order().x(),
        palette="Paired",
        bw_adjust=0.5,
        cut=1,
        linewidth=1,
        fill=True,
    )
    #
    # Title
    #
    g.figure.suptitle(
        ""
        if aes_cfg.base().focus()
        else "Evaluation measures for original ground truths against themselves",
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
        labels=[content.to_label() for content in aes_cfg.ticks_order().x()],
        ha="center",
    )
    g.tight_layout()

    g.savefig(pdf)
    plt.close()
