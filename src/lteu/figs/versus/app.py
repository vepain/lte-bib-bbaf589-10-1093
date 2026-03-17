"""Versus figures applications."""

# Due to typer:
# ruff: noqa: PLR0913

from pathlib import Path
from typing import Annotated

import typer

from lteu import log
from lteu.figs import aes, items, ops

from . import main

APP = typer.Typer(name="vs", help="Versus figures commands.")


class InputsGT:
    """Inputs for gt command."""

    X_AXIS = typer.Option("--x-axis", help="X axis")
    Y_AXIS = typer.Option("--y-axis", help="Y axis")

    X_LABEL = typer.Option("--x-label", help="X axis label")
    Y_LABEL = typer.Option("--y-label", help="Y axis label")

    MEASURE = typer.Argument(help="Measure code")

    PDF = typer.Argument(help="PDF path")


@APP.command(name="gt")
def gt(
    x_evals_tsv: Annotated[Path, InputsGT.X_AXIS],
    y_evals_tsv: Annotated[Path, InputsGT.Y_AXIS],
    x_label: Annotated[str, InputsGT.X_LABEL],
    y_label: Annotated[str, InputsGT.Y_LABEL],
    measure: Annotated[items.MeasureCodes, InputsGT.MEASURE],
    pdf_path: Annotated[Path, InputsGT.PDF],
    # AES
    context: Annotated[aes.SeabornContext, aes.TyperInputs.CONTEXT],
    focus: Annotated[bool, aes.TyperInputs.FOCUS],
) -> None:
    """Versus figure for ground truths."""
    # REVIEW use by default RmSamplesModes.NOTHING
    df = main.get_dataframe_gt(
        x_evals_tsv,
        y_evals_tsv,
        measure,
        ops.RmSamplesModes.NOTHING,
    )

    aes_cfg = main.Aes(aes.Base(context, focus), main.Labels(x_label, y_label))

    pdf_path.parent.mkdir(exist_ok=True, parents=True)

    main.gt(
        df,
        measure,
        aes_cfg,
        pdf_path,
    )

    log.print_done(f"Figure generated: {log.fmt_img(pdf_path)}")
