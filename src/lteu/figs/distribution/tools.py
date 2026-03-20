"""Distribution figure for tools."""

from enum import StrEnum
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb

from lteu import bins, tools
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
        (bins.Contents.ONLY_PLASMIDS, only_plm_df),
        (bins.Contents.WITH_CHROMOSOMES, with_chm_df),
    ):
        new_eval_df = dist_data.replace_measures_cols_to_class_mode_val_cols(
            eval_df,
            [merge_files.Header.SAMPLE_ID, merge_files.Header.TOOL_CODE],
            Columns.MEASURE_CLASS,
            Columns.MEASURE_MODE,
            Columns.VALUE,
        )

        new_eval_df[Columns.CONTENT] = content

        df = pd.concat([df, new_eval_df], ignore_index=True)

    # Keep only tools in list
    df = df[df[Columns.TOOL_CODE].isin(tools)]

    return figs_data.do_remove_samples_strategy(df, remove_samples, Columns.SAMPLE_ID)


class FullOrders:
    """Orders."""

    def __init__(
        self,
        row: list[measures.Class],
        col: list[measures.Mode],
        x: list[tools.Binning],
        hue: tuple[bins.Contents, bins.Contents],
    ) -> None:
        self._row: list[measures.Class] = row
        self._col: list[measures.Mode] = col
        self._x: list[tools.Binning] = x
        self._hue: tuple[bins.Contents, bins.Contents] = hue

    def row(self) -> list[measures.Class]:
        """Get row order."""
        return self._row

    def col(self) -> list[measures.Mode]:
        """Get column order."""
        return self._col

    def x(self) -> list[tools.Binning]:
        """Get x order."""
        return self._x

    def hue(self) -> tuple[bins.Contents, bins.Contents]:
        """Get hue order."""
        return self._hue


class FullAes:
    """Distributions aesthetics."""

    def __init__(
        self,
        base_aes: figs_aes.Base,
        orders: FullOrders,
    ) -> None:
        self._base_aes: figs_aes.Base = base_aes
        self._orders: FullOrders = orders

    def base(self) -> figs_aes.Base:
        """Get base aesthetic configuration."""
        return self._base_aes

    def orders(self) -> FullOrders:
        """Get orders."""
        return self._orders


def full_violins_plot(  # noqa: C901
    df: pd.DataFrame,
    aes_cfg: FullAes,
    remove_samples: figs_data.RmSamplesModes,
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
        legend=False,
        margin_titles=True,
        # Violinplot options
        x=Columns.TOOL_CODE,
        order=aes_cfg.orders().x(),
        hue=Columns.CONTENT,
        hue_order=aes_cfg.orders().hue(),
        palette="Paired",
        bw_adjust=0.5,
        cut=1,
        linewidth=1,
        fill=True,
        split=True,
        gap=0.2,
    )

    #
    # Title
    #
    def get_subtitle() -> str:
        match remove_samples:
            case figs_data.RmSamplesModes.FAILS:
                return f"\n({df[Columns.SAMPLE_ID].nunique()!s} samples)"
            case figs_data.RmSamplesModes.NOTHING:
                return ""

    g.figure.suptitle(
        ""
        if aes_cfg.base().focus()
        else (
            "Evaluation measures for each tool"
            "\nhalf left: only plasmids; half right: with chromosomes" + get_subtitle()
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
    def tool_nsamples_labels() -> dict[tools.Binning, str]:
        match remove_samples:
            case figs_data.RmSamplesModes.FAILS:
                return dict.fromkeys(aes_cfg.orders().x(), "")
            case figs_data.RmSamplesModes.NOTHING:
                labels = {}
                for tool in aes_cfg.orders().x():
                    nsamples = df[df[Columns.TOOL_CODE] == tool][
                        Columns.SAMPLE_ID
                    ].nunique()
                    labels[tool] = f"\n({nsamples})"
                return labels

    sub_x_labels = tool_nsamples_labels()

    g.set_xticklabels(
        labels=[tool.to_label() + sub_x_labels[tool] for tool in aes_cfg.orders().x()],
        ha="center",
    )
    g.tight_layout()

    #
    # Custom colors by x times hue
    #
    colors = sns.color_palette("Paired")

    def fix_violins_colors() -> None:

        def get_axes_violins_indices() -> list[list[int]]:
            # Get violin plots indices ("flat violin plot" <=> no violin plot)
            # According to the row and the columns orders, flattened
            axes_violins_indices: list[list[int]] = []

            for row in aes_cfg.orders().row():
                for col in aes_cfg.orders().col():
                    violin_indices: list[int] = []

                    df_row_col = df[
                        (df[Columns.MEASURE_CLASS] == row)
                        & (df[Columns.MEASURE_MODE] == col)
                    ]

                    for ind, (x, hue) in enumerate(
                        product(aes_cfg.orders().x(), aes_cfg.orders().hue()),
                    ):
                        values = df_row_col[
                            (df_row_col[Columns.TOOL_CODE] == x)
                            & (df_row_col[Columns.CONTENT] == hue)
                        ][Columns.VALUE].to_numpy()

                        if values.shape[0] > 0 and (values[0] != values).any():
                            violin_indices.append(ind)

                    axes_violins_indices.append(violin_indices)

            return axes_violins_indices

        axes_violins_indices = get_axes_violins_indices()

        for ax_ind, ax in enumerate(g.figure.axes):
            for ind, violin in enumerate(ax.findobj(PolyCollection)):
                rgb = to_rgb(colors[axes_violins_indices[ax_ind][ind]])
                violin.set_facecolor(rgb)

    fix_violins_colors()

    g.savefig(pdf)
    plt.close()


def get_content_dataframe(
    only_plm_tools_evals_tsv: Path,
    with_chm_tools_evals_tsv: Path,
    tools: list[tools.Binning],
    remove_samples: figs_data.RmSamplesModes,
    measure_mode: measures.Mode,
) -> pd.DataFrame:
    """Get dataframe for chromosomes bias focus."""
    df = get_dataframe(
        only_plm_tools_evals_tsv,
        with_chm_tools_evals_tsv,
        tools,
        remove_samples,
    )
    return df[df[Columns.MEASURE_MODE] == measure_mode]


class ContentOrders:
    """Orders for chromosomes bias focus."""

    def __init__(
        self,
        row: list[measures.Class],
        col: list[bins.Contents],
        x: list[tools.Binning],
        # hue: tuple[bins.Contents, bins.Contents],
    ) -> None:
        self._row: list[measures.Class] = row
        self._col: list[bins.Contents] = col
        self._x: list[tools.Binning] = x

    def row(self) -> list[measures.Class]:
        """Get row order."""
        return self._row

    def col(self) -> list[bins.Contents]:
        """Get column order."""
        return self._col

    def x(self) -> list[tools.Binning]:
        """Get x order."""
        return self._x


class ContentAes:
    """Distributions aesthetics for chromosomes bias focus."""

    def __init__(
        self,
        base_aes: figs_aes.Base,
        orders: ContentOrders,
    ) -> None:
        self._base_aes: figs_aes.Base = base_aes
        self._orders: ContentOrders = orders

    def base(self) -> figs_aes.Base:
        """Get base aesthetic configuration."""
        return self._base_aes

    def orders(self) -> ContentOrders:
        """Get orders."""
        return self._orders


def content_violins_plot(
    df: pd.DataFrame,
    aes_cfg: ContentAes,
    measure_mode: measures.Mode,
    remove_samples: figs_data.RmSamplesModes,
    pdf: Path,
) -> None:
    """Create a violins plot for the tools comparing bin contents."""
    sns.set_context(aes_cfg.base().context())  # ty:ignore[invalid-argument-type]

    g = sns.catplot(
        data=df,
        y=Columns.VALUE,
        # FacedGrid
        kind="violin",
        row=Columns.MEASURE_CLASS,
        row_order=aes_cfg.orders().row(),
        col=Columns.CONTENT,
        col_order=aes_cfg.orders().col(),
        sharex=True,
        sharey=True,
        legend=False,
        margin_titles=True,
        # Violinplot options
        x=Columns.TOOL_CODE,
        order=aes_cfg.orders().x(),
        hue=Columns.TOOL_CODE,
        hue_order=aes_cfg.orders().x(),
        palette="Set3",
        bw_adjust=0.5,
        cut=1,
        linewidth=1,
        fill=True,
    )

    #
    # Title
    #
    def get_subtitle() -> str:
        match remove_samples:
            case figs_data.RmSamplesModes.FAILS:
                return f"\n({df[Columns.SAMPLE_ID].nunique()!s} samples)"
            case figs_data.RmSamplesModes.NOTHING:
                return ""

    g.figure.suptitle(
        ""
        if aes_cfg.base().focus()
        else (f"{measure_mode} evaluation measures for each tool" + get_subtitle()),
    )
    #
    # Subplot titles
    #
    g.set_titles(col_template="{col_name}", row_template="{row_name}")
    # fix the col titles
    g.figure.axes[0].set_title(aes_cfg.orders().col()[0].to_label())
    g.figure.axes[1].set_title(aes_cfg.orders().col()[1].to_label())

    g.set_xlabels("")
    g.set_ylabels("")

    #
    # Sub X axis tick labels
    #
    def tool_nsamples_labels() -> dict[tools.Binning, str]:
        match remove_samples:
            case figs_data.RmSamplesModes.FAILS:
                return dict.fromkeys(aes_cfg.orders().x(), "")
            case figs_data.RmSamplesModes.NOTHING:
                labels = {}
                for tool in aes_cfg.orders().x():
                    nsamples = df[df[Columns.TOOL_CODE] == tool][
                        Columns.SAMPLE_ID
                    ].nunique()
                    labels[tool] = f"\n({nsamples})"
                return labels

    sub_x_labels = tool_nsamples_labels()

    g.set_xticklabels(
        labels=[tool.to_label() + sub_x_labels[tool] for tool in aes_cfg.orders().x()],
        ha="center",
    )
    g.tight_layout()

    g.savefig(pdf)
    plt.close()


def get_mode_dataframe(
    only_plm_tools_evals_tsv: Path,
    with_chm_tools_evals_tsv: Path,
    tools: list[tools.Binning],
    remove_samples: figs_data.RmSamplesModes,
    content: bins.Contents,
) -> pd.DataFrame:
    """Get dataframe for measures modes."""
    df = get_dataframe(
        only_plm_tools_evals_tsv,
        with_chm_tools_evals_tsv,
        tools,
        remove_samples,
    )
    return df[df[Columns.CONTENT] == content]


class ModeOrders:
    """Orders for measures modes."""

    def __init__(
        self,
        row: list[measures.Class],
        col: list[measures.Mode],
        x: list[tools.Binning],
    ) -> None:
        self._row: list[measures.Class] = row
        self._col: list[measures.Mode] = col
        self._x: list[tools.Binning] = x

    def row(self) -> list[measures.Class]:
        """Get row order."""
        return self._row

    def col(self) -> list[measures.Mode]:
        """Get column order."""
        return self._col

    def x(self) -> list[tools.Binning]:
        """Get x order."""
        return self._x


class ModeAes:
    """Distributions aesthetics for measures modes."""

    def __init__(
        self,
        base_aes: figs_aes.Base,
        orders: ModeOrders,
    ) -> None:
        self._base_aes: figs_aes.Base = base_aes
        self._orders: ModeOrders = orders

    def base(self) -> figs_aes.Base:
        """Get base aesthetic configuration."""
        return self._base_aes

    def orders(self) -> ModeOrders:
        """Get orders."""
        return self._orders


def mode_violins_plot(
    df: pd.DataFrame,
    aes_cfg: ModeAes,
    content: bins.Contents,
    remove_samples: figs_data.RmSamplesModes,
    pdf: Path,
) -> None:
    """Create a violins plot for the tools comparing measures modes."""
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
        legend=False,
        margin_titles=True,
        # Violinplot options
        x=Columns.TOOL_CODE,
        order=aes_cfg.orders().x(),
        hue=Columns.TOOL_CODE,
        hue_order=aes_cfg.orders().x(),
        palette="Set3",
        bw_adjust=0.5,
        cut=1,
        linewidth=1,
        fill=True,
    )

    #
    # Title
    #
    def get_subtitle() -> str:
        match remove_samples:
            case figs_data.RmSamplesModes.FAILS:
                return f"\n({df[Columns.SAMPLE_ID].nunique()!s} samples)"
            case figs_data.RmSamplesModes.NOTHING:
                return ""

    g.figure.suptitle(
        ""
        if aes_cfg.base().focus()
        else (
            f"Evaluation measures for each tool ({content.to_label()})" + get_subtitle()
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
    def tool_nsamples_labels() -> dict[tools.Binning, str]:
        match remove_samples:
            case figs_data.RmSamplesModes.FAILS:
                return dict.fromkeys(aes_cfg.orders().x(), "")
            case figs_data.RmSamplesModes.NOTHING:
                labels = {}
                for tool in aes_cfg.orders().x():
                    nsamples = df[df[Columns.TOOL_CODE] == tool][
                        Columns.SAMPLE_ID
                    ].nunique()
                    labels[tool] = f"\n({nsamples})"
                return labels

    sub_x_labels = tool_nsamples_labels()

    g.set_xticklabels(
        labels=[tool.to_label() + sub_x_labels[tool] for tool in aes_cfg.orders().x()],
        ha="center",
    )
    g.tight_layout()

    g.savefig(pdf)
    plt.close()
