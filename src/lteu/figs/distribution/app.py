"""Distributions figures applications."""

# Due to typer:
# ruff: noqa: PLR0913

from pathlib import Path
from typing import Annotated

import typer

from lteu import log
from lteu import tools as main_tools
from lteu.eval import measures
from lteu.figs import aes as figs_aes
from lteu.figs import data as figs_data

from . import data
from . import ground_truths as gt
from . import tools as dist_tools

APP = typer.Typer(name="dist", help="Distribution figures.")


class InputsGT:
    """Inputs for gt command."""

    ONLY_PLASMIDS_EVAL_TSV = typer.Argument(
        help="Path to the only plasmids evaluation TSV file.",
    )

    WITH_CHROMOSOMES_EVAL_TSV = typer.Argument(
        help="Path to the with chromosomes evaluation TSV file.",
    )

    PDF = typer.Argument(help="PDF path")


@APP.command(name="gt")
def ground_truths(
    only_plm_eval_tsv: Annotated[Path, InputsGT.ONLY_PLASMIDS_EVAL_TSV],
    with_chm_eval_tsv: Annotated[Path, InputsGT.WITH_CHROMOSOMES_EVAL_TSV],
    pdf_path: Annotated[Path, InputsGT.PDF],
    # AES
    context: Annotated[
        figs_aes.SeabornContext,
        figs_aes.TyperInputs.CONTEXT,
    ] = figs_aes.Base.DEF_CONTEXT,
    focus: Annotated[bool, figs_aes.TyperInputs.FOCUS] = figs_aes.Base.DEF_FOCUS,
) -> None:
    """Distribution figure for ground truths."""
    log.print_title("Uniqify ground truths distribution figure")

    log.print_inputs(
        (
            f"Only plasmids eval TSV: {log.fmt_file(only_plm_eval_tsv)}",
            f"With chromosomes eval TSV: {log.fmt_file(with_chm_eval_tsv)}",
            f"Aesthetics:\n* Context: {context}\n* Focus: {focus}",
            f"PDF: {log.fmt_img(pdf_path)}",
        ),
    )

    df = gt.get_dataframe(only_plm_eval_tsv, with_chm_eval_tsv)

    aes_cfg = gt.Aes(
        figs_aes.Base(context, focus),
        gt.Orders(
            row=[
                measures.Class.COMPLETENESS,
                measures.Class.HOMOGENEITY,
            ],
            col=[measures.Mode.UNWEIGHTED, measures.Mode.WEIGHTED],
            x=[data.Contents.ONLY_PLASMIDS, data.Contents.WITH_CHROMOSOMES],
            hue=[
                gt.HueValues.COMPLETENESS_ONLY_PLASMIDS,
                gt.HueValues.COMPLETENESS_WITH_CHROMOSOMES,
                gt.HueValues.HOMOGENEITY_ONLY_PLASMIDS,
                gt.HueValues.HOMOGENEITY_WITH_CHROMOSOMES,
            ],
        ),
    )

    pdf_path.parent.mkdir(exist_ok=True, parents=True)

    gt.violins_plot(df, aes_cfg, pdf_path)

    log.print_done(f"Figure generated: {log.fmt_img(pdf_path)}")


class InputsTools:
    """Inputs for dist command."""

    ONLY_PLASMIDS_EVAL_TSV = typer.Argument(
        help="Path to the only plasmids evaluation TSV file.",
    )
    WITH_CHROMOSOMES_EVAL_TSV = typer.Argument(
        help="Path to the with chromosomes evaluation TSV file.",
    )
    TOOLS = typer.Option(
        "--tool",
        "-t",
        help="Tool code. The violin plots order follows the user tool order ",
    )

    REMOVE_SAMPLES = typer.Option(
        "--remove-samples",
        "-r",
        help="Mode to remove samples from the dataset",
    )

    PDF = typer.Argument(help="PDF path")


@APP.command(name="tools")
def tools_all(
    only_plasmids_tools_evals_tsv: Annotated[
        Path,
        InputsTools.ONLY_PLASMIDS_EVAL_TSV,
    ],
    with_chromosomes_tools_evals_tsv: Annotated[
        Path,
        InputsTools.WITH_CHROMOSOMES_EVAL_TSV,
    ],
    tools: Annotated[
        list[main_tools.Binning],
        InputsTools.TOOLS,
    ],
    pdf_path: Annotated[Path, InputsTools.PDF],
    remove_samples: Annotated[
        figs_data.RmSamplesModes,
        InputsTools.REMOVE_SAMPLES,
    ] = figs_data.RmSamplesModes.NOTHING,
    # AES
    context: Annotated[
        figs_aes.SeabornContext,
        figs_aes.TyperInputs.CONTEXT,
    ] = figs_aes.Base.DEF_CONTEXT,
    focus: Annotated[bool, figs_aes.TyperInputs.FOCUS] = figs_aes.Base.DEF_FOCUS,
) -> None:
    """Distribution figure for tools."""
    log.print_title("Uniqify tools distribution figure")
    log.print_inputs(
        (
            f"Only plasmids eval TSV: {log.fmt_file(only_plasmids_tools_evals_tsv)}",
            (
                f"With chromosomes eval TSV:"
                f" {log.fmt_file(with_chromosomes_tools_evals_tsv)}"
            ),
            f"Aesthetics:\n* Context: {context}\n* Focus: {focus}",
            f"PDF: {log.fmt_img(pdf_path)}",
        ),
    )

    df = dist_tools.get_dataframe(
        only_plasmids_tools_evals_tsv,
        with_chromosomes_tools_evals_tsv,
        tools,
        remove_samples,
    )

    aes_cfg = dist_tools.Aes(
        figs_aes.Base(context, focus),
        dist_tools.Orders(
            row=[
                measures.Class.COMPLETENESS,
                measures.Class.HOMOGENEITY,
            ],
            col=[measures.Mode.UNWEIGHTED, measures.Mode.WEIGHTED],
            x=tools,
            hue=(
                data.Contents.ONLY_PLASMIDS,
                data.Contents.WITH_CHROMOSOMES,
            ),
        ),
    )

    pdf_path.parent.mkdir(exist_ok=True, parents=True)

    dist_tools.violins_plot(df, aes_cfg, pdf_path)

    log.print_done(f"Figure generated: {log.fmt_img(pdf_path)}")
