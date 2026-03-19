"""Versus figures applications."""

# Due to typer:
# ruff: noqa: PLR0913
from pathlib import Path
from typing import Annotated

import typer

from lteu import log
from lteu.figs import aes as figs_aes
from lteu.figs import data as figs_data

from . import aes, main
from . import ground_truths as gt

APP = typer.Typer(name="vs", help="Versus figures.")


class InputsGT:
    """Inputs for gt command."""

    X_AXIS = typer.Option("--x-axis", help="X axis")
    Y_AXIS = typer.Option("--y-axis", help="Y axis")

    X_LABEL = typer.Option("--x-label", help="X axis label")
    Y_LABEL = typer.Option("--y-label", help="Y axis label")

    MEASURE = typer.Argument(help="Measure code")

    PDF = typer.Argument(help="PDF path")


@APP.command(name="gt")
def ground_truths(
    x_evals_tsv: Annotated[Path, InputsGT.X_AXIS],
    y_evals_tsv: Annotated[Path, InputsGT.Y_AXIS],
    x_label: Annotated[str, InputsGT.X_LABEL],
    y_label: Annotated[str, InputsGT.Y_LABEL],
    measure: Annotated[figs_data.MeasureCodes, InputsGT.MEASURE],
    pdf_path: Annotated[Path, InputsGT.PDF],
    # AES
    context: Annotated[
        figs_aes.SeabornContext,
        figs_aes.TyperInputs.CONTEXT,
    ] = figs_aes.Base.DEF_CONTEXT,
    focus: Annotated[bool, figs_aes.TyperInputs.FOCUS] = figs_aes.Base.DEF_FOCUS,
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

    df = gt.get_dataframe(x_evals_tsv, y_evals_tsv, measure)

    aes_cfg = aes.Config(
        figs_aes.Base(context, focus),
        aes.Labels(title=measure.to_label("plural"), x_label=x_label, y_label=y_label),
    )

    pdf_path.parent.mkdir(exist_ok=True, parents=True)

    main.gt(df, aes_cfg, gt.Columns.CLASS, pdf_path)

    log.print_done(f"Figure generated: {log.fmt_img(pdf_path)}")
