"""Distribution figure for tools."""

from enum import StrEnum
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb

from lteu import tools
from lteu.eval import measures
from lteu.eval.merge import files as merge_files
from lteu.eval.run import files as eval_files
from lteu.figs import aes as figs_aes
from lteu.figs import data as figs_data

from . import data as dist_data


class Columns(StrEnum):
    """DataFrame columns."""

    SAMPLE_ID = eval_files.Header.SAMPLE_ID
    TOOL_CODE = merge_files.Header.TOOL_CODE
    CONTENT = "Content"
    MEASURE_CLASS = "Measure class"
    MEASURE_MODE = "Measure mode"
    VALUE = "Value"
    HUE = "hue"


def get_dataframe(
    only_plm_tools_evals_tsv: Path,
    with_chm_tools_evals_tsv: Path,
    tools: list[tools.Binning],
    remove_samples: figs_data.RmSamplesModes,
) -> pd.DataFrame:
    """Get the dataframe for a distribution figure for tools."""
    only_plm_df = merge_files.to_dataframe(only_plm_tools_evals_tsv)
    with_chm_df = merge_files.to_dataframe(with_chm_tools_evals_tsv)

    df = pd.DataFrame(columns=list(Columns))

    for content, eval_df in (
        (dist_data.Contents.ONLY_PLASMIDS, only_plm_df),
        (dist_data.Contents.WITH_CHROMOSOMES, with_chm_df),
    ):
        new_eval_df = dist_data.replace_measures_cols_to_class_mode_val_cols(
            eval_df,
            [merge_files.Header.TOOL_CODE],
            Columns.MEASURE_CLASS,
            Columns.MEASURE_MODE,
            Columns.VALUE,
        )

        new_eval_df[Columns.CONTENT] = content

        df = pd.concat([df, new_eval_df], ignore_index=True)

    # Keep only tools in list
    df = df[df[Columns.TOOL_CODE].isin(tools)]

    return figs_data.do_remove_samples_strategy(df, remove_samples, Columns.SAMPLE_ID)


class Orders:
    """Orders."""

    def __init__(
        self,
        row: list[measures.Class],
        col: list[measures.Mode],
        x: list[tools.Binning],
        hue: tuple[dist_data.Contents, dist_data.Contents],
    ) -> None:
        self._row: list[measures.Class] = row
        self._col: list[measures.Mode] = col
        self._x: list[tools.Binning] = x
        self._hue: tuple[dist_data.Contents, dist_data.Contents] = hue

    def row(self) -> list[measures.Class]:
        """Get row order."""
        return self._row

    def col(self) -> list[measures.Mode]:
        """Get column order."""
        return self._col

    def x(self) -> list[tools.Binning]:
        """Get x order."""
        return self._x

    def hue(self) -> tuple[dist_data.Contents, dist_data.Contents]:
        """Get hue order."""
        return self._hue


class Aes:
    """Distributions aesthetics."""

    def __init__(
        self,
        base_aes: figs_aes.Base,
        orders: Orders,
    ) -> None:
        self._base_aes: figs_aes.Base = base_aes
        self._orders: Orders = orders

    def base(self) -> figs_aes.Base:
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
    """Create a violins plot for the tools."""
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
        # Violinplot options
        x=Columns.CONTENT,
        order=aes_cfg.orders().x(),
        hue=Columns.CONTENT,
        hue_order=aes_cfg.orders().hue(),
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
        labels=[content.to_label() for content in aes_cfg.orders().x()],
        ha="center",
    )
    g.tight_layout()

    #
    # Custom colors by x times hue
    #
    colors = sns.color_palette("Paired")
    for ax in g.figure.axes:
        for ind, violin in enumerate(ax.findobj(PolyCollection)):
            rgb = to_rgb(colors[ind])
            violin.set_facecolor(rgb)

    g.savefig(pdf)
    plt.close()
