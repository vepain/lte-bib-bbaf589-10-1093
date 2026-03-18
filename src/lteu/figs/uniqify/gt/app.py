"""Versus figures applications."""

# Due to typer:
# ruff: noqa: PLR0913
from pathlib import Path
from typing import Annotated

import typer

from lteu import log
from lteu.figs import aes, items
from lteu.figs.versus import main as vs_main

from . import distribution, versus

APP = typer.Typer(name="gt", help="Uniqify ground truths experiment figures.")


class InputsVersus:
    """Inputs for versus command."""

    X_AXIS = typer.Option("--x-axis", help="X axis")
    Y_AXIS = typer.Option("--y-axis", help="Y axis")

    X_LABEL = typer.Option("--x-label", help="X axis label")
    Y_LABEL = typer.Option("--y-label", help="Y axis label")

    MEASURE = typer.Argument(help="Measure code")

    PDF = typer.Argument(help="PDF path")


@APP.command(name="vs")
def vs(
    x_evals_tsv: Annotated[Path, InputsVersus.X_AXIS],
    y_evals_tsv: Annotated[Path, InputsVersus.Y_AXIS],
    x_label: Annotated[str, InputsVersus.X_LABEL],
    y_label: Annotated[str, InputsVersus.Y_LABEL],
    measure: Annotated[items.MeasureCodes, InputsVersus.MEASURE],
    pdf_path: Annotated[Path, InputsVersus.PDF],
    # AES
    context: Annotated[aes.SeabornContext, aes.TyperInputs.CONTEXT],
    focus: Annotated[bool, aes.TyperInputs.FOCUS],
) -> None:
    """Versus figure for ground truths."""
    log.print_title("Uniqify ground truths versus figure")
    log.print_inputs(
        (
            f"X label: {x_label}",
            f"X evals TSV: {log.fmt_file(x_evals_tsv)}",
            f"Y label: {y_label}",
            f"Y evals TSV: {log.fmt_file(y_evals_tsv)}",
            f"Measure: {measure}",
            f"Aesthetics:\n* Context: {context}\n* Focus: {focus}",
            f"PDF: {log.fmt_img(pdf_path)}",
        ),
    )

    df = versus.get_dataframe(x_evals_tsv, y_evals_tsv, measure)

    aes_cfg = vs_main.Aes(
        aes.Base(context, focus),
        vs_main.Labels(measure.to_label("plural"), x_label, y_label),
    )

    pdf_path.parent.mkdir(exist_ok=True, parents=True)

    vs_main.gt(df, aes_cfg, pdf_path)

    log.print_done(f"Figure generated: {log.fmt_img(pdf_path)}")


class InputsDistribution:
    """Inputs for dist command."""

    ONLY_PLASMIDS_EVAL_TSV = typer.Argument(
        help="Path to the only plasmids evaluation TSV file.",
    )

    WITH_CHROMOSOMES_EVAL_TSV = typer.Argument(
        help="Path to the with chromosomes evaluation TSV file.",
    )

    PDF = typer.Argument(help="PDF path")


@APP.command(name="dist")
def dist(
    only_plm_eval_tsv: Annotated[Path, InputsDistribution.ONLY_PLASMIDS_EVAL_TSV],
    with_chm_eval_tsv: Annotated[Path, InputsDistribution.WITH_CHROMOSOMES_EVAL_TSV],
    pdf_path: Annotated[Path, InputsDistribution.PDF],
    # AES
    context: Annotated[aes.SeabornContext, aes.TyperInputs.CONTEXT],
    focus: Annotated[bool, aes.TyperInputs.FOCUS],
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

    df = distribution.get_dataframe(only_plm_eval_tsv, with_chm_eval_tsv)

    aes_cfg = distribution.Aes(
        aes.Base(context, focus),
        distribution.TicksOrder(
            [
                distribution.MeasureClass.COMPLETENESS,
                distribution.MeasureClass.HOMOGENEITY,
            ],
            [distribution.MeasureMode.UNWEIGHTED, distribution.MeasureMode.WEIGHTED],
            [items.Contents.ONLY_PLASMIDS, items.Contents.WITH_CHROMOSOMES],
        ),
    )

    pdf_path.parent.mkdir(exist_ok=True, parents=True)

    distribution.violins_plot(df, aes_cfg, pdf_path)

    log.print_done(f"Figure generated: {log.fmt_img(pdf_path)}")
